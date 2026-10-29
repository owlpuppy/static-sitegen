if python3 src/main.py --verbose; then
    cd public && python3 -m http.server 8888
else
    echo "test build failed, skipping webserver start on localhost"
fi
