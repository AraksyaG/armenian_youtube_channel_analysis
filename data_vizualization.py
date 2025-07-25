import psycopg2
import pandas as pd
import matplotlib.pyplot as plt

# Connect to your PostgreSQL database
conn = psycopg2.connect(
    host="localhost",
    database="youtube_database",
    user="postgres",
    password="2005",
    port=5432
)

query1 = """
select * from youtube_channels;
"""
query2 = """
select * from videos;
"""

channels = pd.read_sql(query1, conn)
videos= pd.read_sql(query2, conn)
# print(channels['channel_name'])
# print(videos.head())

videos = videos.merge(
    channels[['channel_id', 'channel_name']],
    on='channel_id',
    how='left'
)

"""
Vizualizations
"""
# Average View Growth Across All Videos (2nd Day After Publish)
videos['published_at'] = pd.to_datetime(videos['published_at'])
videos['scraped_at'] = pd.to_datetime(videos['scraped_at'])
videos['days_after_pub'] = abs(videos['published_at'] - videos['scraped_at']).dt.days
day2_views = videos[(videos['days_after_pub'] >= 2) & (videos['days_after_pub'] <= 4)]


day2_views = day2_views.drop_duplicates(subset=['original_video_id'])

avg_views_per_channel = day2_views.groupby('channel_name')['views'].mean()

plt.bar(x=avg_views_per_channel.index, height=avg_views_per_channel.values)
plt.title('Average views per channel')
plt.xlabel('Channel')
plt.ylabel('Views')
plt.xticks(rotation=90)
plt.tight_layout()
# plt.show()

# Rating Distribution
day10_views = videos[videos['days_after_pub'] <= 10]
day10_views = day10_views.drop_duplicates(subset=['original_video_id'])
ratings_per_channel = day10_views.groupby('channel_name')['rating'].mean()

plt.bar(ratings_per_channel.index, ratings_per_channel.values)
plt.title('Average ratings per channel')
plt.xlabel('Channel')
plt.ylabel('Ratings')
plt.xticks(rotation=90)
plt.tight_layout()
# plt.show()

# Views vs Rating
within_10_days = day10_views.sort_values(['original_video_id', 'scraped_at'])
within_10_days = within_10_days.groupby('original_video_id').tail(1)

# for channel, group in within_10_days.groupby('channel_name'):
#     plt.figure(figsize=(8, 5))
#     plt.scatter(group['views'], group['rating'], label=channel)
#     plt.title("Views vs Ratings (Last Record Within First 10 Days per Video)")
#     plt.xlabel("Views")
#     plt.ylabel("Ratings")
#     plt.legend(title='Channel', loc='upper right')
#     plt.tight_layout()
#     plt.show()

for channel, group in within_10_days.groupby('channel_name'):
    corr = group['views'].corr(group['rating'])
    # print(f'{channel}: {corr}')


# Videos Published Over Time
videos['week'] = videos['published_at'].dt.to_period('W').apply(lambda r: r.start_time)
videos_unique = videos.drop_duplicates(subset=['original_video_id'])
weekly_counts = videos_unique.groupby(['channel_name', 'week']).size().reset_index(name='counts')
avg_weekly_uploads = weekly_counts.groupby('channel_name')['counts'].mean()


plt.bar(avg_weekly_uploads.index, avg_weekly_uploads.values)
plt.title('Average weekly uploads per channel')
plt.xlabel('Channel')
plt.ylabel('Uploads')
plt.xticks(rotation=90)
plt.tight_layout()
# plt.show()


# Uploads per Channel
videos_unique = videos.drop_duplicates(subset='original_video_id')

upload_counts = videos_unique['channel_name'].value_counts().sort_values(ascending=False)

plt.figure(figsize=(12, 6))
plt.bar(upload_counts.index, upload_counts.values)
plt.title('Total Uploaded Videos per Channel')
plt.xlabel('Channel')
plt.ylabel('Number of Videos')
plt.xticks(rotation=90)
plt.tight_layout()
# plt.show()

# View Growth Curve Example (Per Channel)
videos = videos[videos['days_after_pub'] >= 0]
avg_views_by_day = videos.groupby(['channel_name', 'days_after_pub'])['views'].mean().reset_index()
channels = avg_views_by_day['channel_name'].unique()
for channel in channels:
    channel_data = avg_views_by_day[avg_views_by_day['channel_name'] == channel]
    plt.figure(figsize=(8, 4))
    plt.plot(channel_data['days_after_pub'], channel_data['views'], marker='o')
    plt.title(f"View Growth Over Time: {channel}")
    plt.xlabel("Days After Publication")
    plt.ylabel("Average Views")
    plt.grid(True)
    plt.tight_layout()
    # plt.show()

conn.close()

