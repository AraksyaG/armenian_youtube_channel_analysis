import os
from xml.etree import ElementTree
from datetime import datetime
from pathlib import Path
import psycopg2


def parse_xml_file(file_path):
    try:
        tree = ElementTree.parse(file_path)
        root = tree.getroot()

        # Extract channel name, date, and timestamp from filename
        filename = os.path.basename(file_path).replace('.xml', '')
        parts = filename.rsplit('_', 2)

        if len(parts) != 3:
            print(f"Unexpected filename format: {filename}")
            return None

        channel_name_raw, file_date_str, timestamp = parts
        channel_name = channel_name_raw.replace('_', ' ')
        file_date = datetime.strptime(file_date_str, "%Y-%m-%d").date()

        ns = {
            'yt': 'http://www.youtube.com/xml/schemas/2015',
            'media': 'http://search.yahoo.com/mrss/',
            'atom': 'http://www.w3.org/2005/Atom'
        }

        # # Get original_channel_id
        # original_channel_id_element = root.find('yt:channelId', ns)
        # if original_channel_id_element is None or not original_channel_id_element.text.strip():
        #     print(f"Missing original_channel_id in file {filename}")
        #     return None
        # original_channel_id = original_channel_id_element.text.strip()

        # Properly extract channel URL from <link rel="alternate">
        channel_url = None
        for link in root.findall('atom:link', ns):
            if link.attrib.get('rel') == 'alternate':
                channel_url = link.attrib.get('href')
                break

        if not channel_url:
            print(f"Missing channel URL in file {filename}")
            return None

        videos = []
        for entry in root.findall('atom:entry', ns):
            media_group = entry.find('media:group', ns)

            title = media_group.find('media:title', ns).text if media_group is not None else ''
            description = media_group.find('media:description', ns).text if media_group is not None else ''

            stats_tag = media_group.find('media:community/media:statistics', ns) if media_group is not None else None
            views = int(stats_tag.attrib.get('views', 0)) if stats_tag is not None else 0

            rating_tag = media_group.find('media:community/media:starRating', ns) if media_group is not None else None
            rating = int(rating_tag.attrib.get('count', 0)) if rating_tag is not None else 0

            video_id = entry.find('yt:videoId', ns)
            video_url_element = entry.find('atom:link', ns)
            published_element = entry.find('atom:published', ns)

            if video_id is None or video_url_element is None or published_element is None:
                continue

            video_data = {
                'original_video_id': video_id.text,
                'title': title,
                'description': description,
                'published': published_element.text,
                'url': video_url_element.attrib.get('href'),
                'views': views,
                'rating': rating
            }
            videos.append(video_data)

        return {
            'channel_name': channel_name,
            'original_channel_id': channel_url[32:],
            'channel_url': channel_url,
            'file_date': file_date,
            'scrape_date': file_date,
            'videos': videos
        }

    except Exception as e:
        print(f"Error parsing {file_path}: {str(e)}")
        return None


def upsert_channel(cursor, channel_data):
    try:
        cursor.execute("""
            INSERT INTO youtube_channels 
            (original_channel_id, channel_name, url, last_scraped)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (url) DO UPDATE SET
                channel_name = EXCLUDED.channel_name,
                original_channel_id = EXCLUDED.original_channel_id,
                last_scraped = EXCLUDED.last_scraped
            RETURNING channel_id
        """, (
            channel_data['original_channel_id'],
            channel_data['channel_name'],
            channel_data['channel_url'],
            channel_data['scrape_date']
        ))
        return cursor.fetchone()[0]
    except Exception as e:
        print(f"ERROR in channel upsert: {str(e)}")
        raise


def insert_videos(cursor, videos, channel_id, scrape_date):
    inserted = 0
    for video in videos:
        try:
            try:
                published_date = datetime.fromisoformat(video['published']).date()
            except ValueError:
                published_date = scrape_date

            cursor.execute("""
                INSERT INTO videos (
                    original_video_id, channel_id, title, description,
                    published_at, url, views, rating, scraped_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                video['original_video_id'],
                channel_id,
                video['title'],
                video['description'],
                published_date,
                video['url'],
                video['views'],
                video['rating'],
                scrape_date
            ))
            inserted += 1
        except Exception as e:
            print(f"ERROR inserting video {video.get('original_video_id')}: {str(e)}")
            continue
    return inserted


def main():
    conn = None
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="youtube_database",
            user="postgres",
            password="2005",
            port=5432
        )

        xml_folder = Path("C:/Users/User/Desktop/youtube_channel_analysis/XML_Files")
        stats = {
            'total_files': 0,
            'channels_processed': 0,
            'videos_inserted': 0,
            'failed_files': 0
        }

        for file_path in xml_folder.glob("*.xml"):
            stats['total_files'] += 1
            print(f"\nProcessing file {stats['total_files']}: {file_path.name}")

            with conn:
                with conn.cursor() as cursor:
                    try:
                        data = parse_xml_file(file_path)
                        if not data:
                            stats['failed_files'] += 1
                            continue

                        channel_id = upsert_channel(cursor, data)
                        stats['channels_processed'] += 1
                        print(f"Channel ID: {channel_id}")

                        inserted = insert_videos(cursor, data['videos'], channel_id, data['scrape_date'])
                        stats['videos_inserted'] += inserted
                        print(f"Inserted {inserted} videos")

                    except Exception as e:
                        stats['failed_files'] += 1
                        print(f"FAILED to process {file_path.name}: {str(e)}")

        print("\nPROCESSING COMPLETE")
        print(f"Total files processed: {stats['total_files']}")
        print(f"Channels processed: {stats['channels_processed']}")
        print(f"Videos inserted: {stats['videos_inserted']}")
        print(f"Failed files: {stats['failed_files']}")

    except Exception as e:
        print(f"FATAL ERROR: {str(e)}")
    finally:
        if conn is not None:
            conn.close()


if __name__ == "__main__":
    main()
