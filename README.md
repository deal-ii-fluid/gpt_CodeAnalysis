
# Minimal example for gpt_code_analysis

## 
```
poetry add xxx
vim .env // add OPENAI_API_KEY=sk-
```

## 建造轮子
```bash
nix develop
nix shell nixpkgs#poetry --command poetry build --format=wheel #poetry build --format=wheel
```

## 制作python环境镜像
```bash
podman \
build \
--file Containerfile \
--tag gpt_analysis:0.0.1
```

## 启动podman image
```podman machine stop; podman machine start
```
If restart doesn't help then try to recreate your podman machine:
```
podman machine stop
podman machine rm
podman machine init # you may specify parameters for your VM
podman machine start
```




```bash
podman \
run \
--interactive=true \
--tty=true \
--rm=true \
--user='0' \
--volume="$(pwd)":/code:rw \
--workdir=/code \
gpt_analysis:0.0.1 \
bash \
-c \
"python -c 'from my_package.code_analysis import start; start()'"
```


