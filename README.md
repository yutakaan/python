# python

## OverView
RaspberryPiを使ったスマートホームアプリケーションです。結果はLINEで通知されます。
* getPicture.sh/getPicture.py: RaspberriPiに繋いでいるWebカメラで写真を撮ります。
* interphone.py: インターフォンが鳴ったらLINEに通知されます。
* trainDelay.py: 電車の遅延情報がLINEで通知されます。
* weather.py: ~~天気情報をLINEで通知していましたが、[livedoor天気](https://help.livedoor.com/weather/index.html)のサービス終了に伴い、利用できなくなっています。~~ 翌日の天気を取得して、LINEに通知されます（気象庁のAPIが利用できるようになったので、そちらに対応しています）。デフォルトでは埼玉県南部の設定になっています。
* gitNews.py: Yahoo!のページから主要ニュースのタイトルを取得します。

## Requirement
* RaspberryPi2 Model B
* Python3.X
* WebCamera（Logicool C270n HD 720P で動作確認済み）

## Usage
### Install
<pre>
git clone https://github.com/yutakaan/python.git
</pre>

### Setting
#### logfunc.py
ログの出力場所を各自の環境に合わせて設定してください。
<pre>
log_dir = os.path.expanduser('~') + '/python/log'
</pre>

#### jsonfunc.py
路線名を記載してください（例：埼京線）。[こちら](https://rti-giken.jp/fhc/api/train_tetsudo/)のサイトからデータを取得しています。
trainDelay.py実行時に引数を指定することで、その路線名の情報を取得することができます。指定しない場合は、jsonfunc.pyの路線名の結果が通知されます。
<pre>
# 路線名を記載
TRAIN_ROUTE = ''
</pre>

以下のURLのXXに各自の都道府県コードを入力してください。また、AREA_MODEについては対象地域に合わせて、適宜修正してください。DATE_MODE=1は翌日を意味しています。
<pre>
WEATHER_URL = 'https://www.jma.go.jp/bosai/forecast/data/forecast/XX0000.json'
DATE_MODE = 1
AREA_MODE = 1
</pre>

#### token.py
subfuncフォルダ下にファイルを作成して、Lineのアクセスコードを記載してください。[LINE Notify](https://notify-bot.line.me/ja/)の機能を使っています。
<pre>
ACCESS_TOKEN = ''
</pre>

#### getPicture.py
ログの出力先の設定~~と、写真を送る時間帯を設定~~してください。
<pre>
# set Picture
IMAGE_PATH = os.path.expanduser('~') + '/python/log/'
</pre>

#### interphone.py
高い音、低い音がそれぞれ1回ずつ鳴ったときに通知されます。各家庭のインターフォンの音の周波数や音の大きさに合わせて設定してください。
<pre>
FREQ_HIGH_BASE = 844.16  # high tone frequency
FREQ_LOW_BASE = 680.02   # low tone frequency
</pre>
<pre>
# 振幅設定
AMP_MAX = 0.025
AMP_MIN = 0.02
</pre>
別の雑音が大きい場合は、バンドパスフィルタで制御可能です。
各家庭の状況に合わせて、チューニングを行ってください。
不要な場合はコメントアウトをお願いします。
<pre>
# フィルタ係数
FPASS1 = np.array([670, 860]) # 通過域端周波数
FSTOP1 = np.array([600, 950]) # 阻止域端周波数
FPASS2 = np.array([835, 860]) # 通過域端周波数
FSTOP2 = np.array([750, 950]) # 阻止域端周波数
GPASS = 6   # 通過域端最大損失
GSTOP = 30  # 通過域端最小損失
</pre>

#### trainDelay.py
dataフォルダを作成し、その配下に[こちら](https://rti-giken.jp/fhc/api/train_tetsudo/)のtrain.tsvを配置してください。実行前のチェックで、路線名が正しいかをチェックしています。

### Run
#### getPicture.py/getTrainDelay.py/weather.py/getNews.py
cronに設定しておくことで、定期的に結果をLINEに通知します。
getPicture.sh/getNews.pyは実行時の引数に1を付与することで、LINEへ通知されます。
LINEヘ通知したくない場合は、0を指定してください。
<pre>
# Weather
10 21 * * * python3 $HOME/python/weather.py

# getPicture
0 0-7 * * * $HOME/python/getPicture.sh 0
0 8-19 * * * $HOME/python/getPicture.sh 1
0 20-23 * * * $HOME/python/getPicture.sh 0

# getTrainDelay
20  7 * * * python3 $HOME/python/trainDelay.py

# getNews
30 0-7 * * * python3 $HOME/python/getNews.py 0
30 8,14,20 * * * python3 $HOME/python/getNews.py 1
30 9-13 * * * python3 $HOME/python/getNews.py 0
30 15-19 * * * python3 $HOME/python/getNews.py 0
30 21-23 * * * python3 $HOME/python/getNews.py 0
</pre>

#### interphone.py
常時起動させておきます。
<pre>
sudo vi /etc/systemd/system/interphone.service
</pre>
<pre>
[Unit]
Description=interphone

[Service]
ExecStart=python3 ~/python/interphone.py &
Restart=always
User=pi

[Install]
WantedBy=multi-user.target
</pre>
<pre>
sudo systemctl start interphone.service
sudo systemctl enable interphone.service
</pre>

## Reference
* [ラズベリーパイでインターホンの音を検知する](https://westgate-lab.hatenablog.com/entry/2019/12/25/225422)
* [鉄道遅延情報のjson](https://rti-giken.jp/fhc/api/train_tetsudo/)
* [ラズパイでpython3にopencvを入れたらエラーが出た【対処法】](https://qiita.com/XM03/items/48463fd910470b226f22)
