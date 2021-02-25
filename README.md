# python

## OverView
RaspberryPiを使ったスマートホームアプリケーションです。結果はLINEで通知されます。
* getPicture.sh/getPicture.py: RaspberriPiに繋いでいるWebカメラで写真を撮ります。
* interphone.py: インターフォンが鳴ったらLINEに通知されます。
* trainDelay.py: 電車の遅延情報がLINEで通知されます。
* weather.py: 天気情報をLINEで通知していましたが、[livedoor天気](https://help.livedoor.com/weather/index.html)のサービス終了に伴い、利用できなくなっています。

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
<pre>
# 路線名を記載
TRAIN_ROUTE = ''
</pre>

#### linefunc.py
Lineのアクセスコードを記載してください。[LINE Notify](https://notify-bot.line.me/ja/)の機能を使っています。
<pre>
# Lineのアクセスコード
URL = "https://notify-api.line.me/api/notify"
ACCESS_TOKEN = ''
</pre>

#### getPicture.py
ログの出力先の設定と、写真を送る時間帯を設定してください。
<pre>
# set Picture
IMAGE_PATH = os.path.expanduser('~') + '/python/log/'
PUSH_START = '08'  # 写真送信開始時刻
PUSH_STOP = '19'  # 写真送信終了時刻
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

### Run
#### getPicture.py/getTrainDelay.py
cronに設定しておくことで、定期的に結果をLINEに通知します。
<pre>
# getPicture
0 */1 * * * $HOME/python/getPicture.sh

# getTrainDelay
20  7 * * * python3 $HOME/python/trainDelay.py
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
