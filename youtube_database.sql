drop table if exists videos;
drop table if exists youtube_channels;

create table youtube_channels (
    channel_id SERIAL PRIMARY KEY,
    original_channel_id TEXT UNIQUE,
    channel_name TEXT,
    url TEXT,
    created_at DATE,
    last_scraped DATE
);

create table videos (
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

select * from videos;
