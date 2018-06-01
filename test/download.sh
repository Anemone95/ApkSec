#! /usr/bin/env bash

TOOL_DIR="$( cd "$( dirname "$0"  )" && pwd  )"
python $TOOL_DIR/android-apps-crawler/downloader/downloader.py $TOOL_DIR/android-apps-crawler/repo/databases/anzhi.com.db $TOOL_DIR/android-apps-crawler/repo/apps
