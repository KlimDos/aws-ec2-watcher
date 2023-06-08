# aws-ec2-watcher
Check is any of EC2 instances is running more then expected and stop it

# build:
```
bash build_manual.sh
```



# run locally:
```
docker run \
-e EC2_MAX_HOURS=1 \
-e AWS_ACCESS_KEY_ID="ABCDEFG" \
-e AWS_SECRET_ACCESS_KEY="123abcABC" \
klimdos/aws-ec2-watcher:<latest-tag>

```

# run in k8s:

```
apiVersion: batch/v1
kind: CronJob
metadata:
  name: aws-ec2-watcher-cronjob
spec:
  schedule: "*/10 * * * *"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: aws-ec2-watcher-main-container
            image: klimdos/aws-ec2-watcher:0.0.1.0-ge6c2f17
            envFrom:
            - secretRef:
                name: aws-ec2-watcher-secret
            resources:
              requests:
                cpu: 5m
                memory: '128Mi'
              limits:
                memory: "128Mi"
                cpu: "100m"
          restartPolicy: OnFailure

```

### ssecret:

```
apiVersion: v1
kind: Secret
metadata:
  name: aws-ec2-watcher-secret
data:
  EC2_MAX_HOURS: <base64> (optional)
  AWS_ACCESS_KEY_ID: <base64>
  AWS_SECRET_ACCESS_KEY: <base64>
```