echo "Starting server ..."
python3.4 server.py &
sleep 2
echo "Starting client ..."
python3.4 client.py &

sleep 3
read -p "Press enter to terminate. " answer

kill %1
kill %2

