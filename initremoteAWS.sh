for s in `cat iplist.txt` ; do
   scp -o "StrictHostKeyChecking no" -i $1 -r ./scripts ubuntu@$s:/home/ubuntu
   ssh -n -f -i $1 ubuntu@$s "sh -c 'cd ~/scripts; sudo nohup sh initlocal.sh >/dev/null 2>&1 < /dev/null &'"
done