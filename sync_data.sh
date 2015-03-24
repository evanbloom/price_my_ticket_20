today=$(date +%Y_%m_%d) 
yesterday=$(date -d "yesterday" +%Y_%m_%d)
echo $today
echo $yesterday
mkdir ~/${today}
aws s3 cp ~/${yesterday} s3://ticketdata/${yesterday} --recursive
rm -rf   ~/${yesterday} 
