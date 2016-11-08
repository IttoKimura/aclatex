# aclatex
Auto Complier tool for LaTex

## How to use
aclatex.yamlに以下の設定を記述する
* file_name: 監視したいファイル名
* dir_path : 監視したいファイルのあるディレクトリへの絶対パス
* interval : ファイル監視のインターバル

### Sample
``` yaml
file_name: sample.tex    # 監視するファイル
dir_path: /home/sample/   # sample.texのあるディレクトリ
interval: 2    # 2秒のインターバル
```
続いて、以下のコマンドを実行
``` shell
python aclatex.py
```
