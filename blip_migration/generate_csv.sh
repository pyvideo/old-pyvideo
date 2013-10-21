#!/bin/bash

echo "select videos_video.id,videos_category.title,videos_video.title,videos_video.source_url from videos_video, videos_category where videos_video.category_id = videos_category.id and videos_video.source_url like '%blip.tv%';" | mysql pyvideo
