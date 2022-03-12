for s in `cat iplistreg.txt` ; do
   scp -o "StrictHostKeyChecking no" -i $1 -r ./scripts root@$s:/root
   ssh -n -f -i $1 root@$s "sh -c 'cd scripts; sudo nohup sh initlocal.sh >/dev/null 2>&1 < /dev/null &'"
done