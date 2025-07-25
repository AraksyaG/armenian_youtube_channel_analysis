TRUNCATE videos, youtube_channels RESTART IDENTITY CASCADE;

DROP TABLE IF EXISTS videos;
DROP TABLE IF EXISTS youtube_channels;


CREATE TABLE youtube_channels (
    channel_id SERIAL PRIMARY KEY,
    original_channel_id TEXT unique,
    channel_name TEXT,
    url TEXT,
    last_scraped DATE
);

CREATE TABLE videos (
    video_id SERIAL PRIMARY KEY,
    original_video_id TEXT,
    channel_id INTEGER REFERENCES youtube_channels(channel_id),
    title TEXT,
    description TEXT,
    published_at DATE,
    url TEXT,
    views INTEGER,
    rating INTEGER,
    scraped_at DATE
);



Select * from videos;
select * from youtube_channels;

create materialized view channels as
select * from youtube_channels
where last_scraped > '2025-04-04';

select * from channels;

-- Channels with max/min views
select y.channel_name, min(v.views), max(v.views)
from (
    select distinct on (original_video_id) *
    from videos
    order by original_video_id, scraped_at desc
) v
join youtube_channels y on v.channel_id = y.channel_id
group by y.channel_name;

-- Channels with max/min rating
select y.channel_name, min(v.rating), max(v.rating)
from (
    select distinct on (original_video_id) *
    from videos
    order by original_video_id, scraped_at desc
) v
join youtube_channels y on v.channel_id = y.channel_id
group by y.channel_name;

-- The Number of Distinct Channels in DB
select distinct channel_name
from youtube_channels;

-- How Popular the Channels are
select y.channel_name, sum(v.views) as total_latest_views
from (
    select distinct on (original_video_id) *
    from videos
    order by original_video_id, scraped_at desc
) v
join youtube_channels y on v.channel_id = y.channel_id
group by y.channel_name
order by total_latest_views desc;

-- Top Videos by Views
select distinct(v.title), v.views, y.channel_name, v.scraped_at as last_check
from videos as v
join youtube_channels as y on y.channel_id = v.channel_id
order by views desc
limit 10;


-- Average Views per Channel (based on last scraping date)
select distinct(y.channel_name), avg(v.views)::integer as average_views
from videos as v
join channels as y on y.channel_id = v.channel_id
where v.scraped_at::date = v.published_at::date + INTERVAL '2 days'
group by y.channel_name
order by avg(v.views)::integer desc;

-- Missing Descriptions or Titles
select count(*) as missing_title_count
from videos
where title is null or title = '';

select count(*) as missing_description_count
from videos
where description is null or description = '';

-- Number of Videos Publishes Over Time (for python)
select y.channel_name, v.published_at as publish_date, count(distinct(v.original_video_id)) as video_count
from youtube_channels as y
join videos as v on v.channel_id = y.channel_id
group by y.channel_name, v.published_at
order by video_count desc;

-- Views Trend Over Time (when most view generating videos are being posted)

select published_at as publish_date, sum(views) as total_views
from videos
group by publish_date
order by total_views desc;

-- Average Rating per Channel (based on last scraping date)
select distinct(y.channel_name), avg(v.rating)::integer as average_views
from videos as v
join youtube_channels as y on y.channel_id = v.channel_id
where v.scraped_at::date = v.published_at::date + INTERVAL '2 days'
group by y.channel_name
order by avg(v.rating)::integer desc;

-- Duplicate Videos
select original_video_id, title, count(scraped_at) as number_of_days_scraped
from videos
group by original_video_id, title, scraped_at
having count(scraped_at) > 1;

-- Channel Without Videos
select y.channel_name
from youtube_channels as y
left join videos as v on v.channel_id = y.channel_id
where v.video_id is null;














