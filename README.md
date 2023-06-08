# aws-ec2-watcher
Check is any of EC2 instances is running more then expected and stop it

```
docker run \
-e EC2_MAX_HOURS=1 \
-e AWS_ACCESS_KEY_ID="ABCDEFG" \
-e AWS_SECRET_ACCESS_KEY="123abcABC" \
klimdos/aws-ec2-watcher:<latest-tag>

```