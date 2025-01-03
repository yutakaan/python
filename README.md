# python
## 概要
RaspberryPiを使ったスマートホームアプリケーション群です。結果をLINEで通知させることができます。
## スペック
* RaspberryPi2 Model B
* Python3.7.3
* WebCamera（Logicool C270n HD 720P で動作確認済み）
* 太陽光HEMSモニタ（オムロン製：KP-MU1P-SET）
* SwitchBot 温湿度計
* SwitchBot CO2センサー（温湿度計）
## インストール方法
<pre>
git clone https://github.com/yutakaan/python.git
</pre>
## アプリの説明
### getPicture.sh/getPicture.py
#### 概要
* RaspberriPiに繋いでいるWebカメラで写真を撮ります。
* シェルの内部でpythonを実行しています。
* ログの出力先の設定~~と、写真を送る時間帯を設定~~してください。
<pre>
# set Picture
IMAGE_PATH = os.path.expanduser('~') + '/python/log/'
</pre>
#### 実行方法
* 引数によってLINEに通知するかしないかを選択できます。
<pre>
$HOME/python/getPicture.sh 0 # LINEに通知しない
$HOME/python/getPicture.sh 1 # LINEに通知する
</pre>
### interphone.py
#### 概要
* インターフォンが鳴ったらLINEに通知されます。
* 高い音、低い音がそれぞれ1回ずつ鳴ったときに通知されます。各家庭のインターフォンの音の周波数や音の大きさに合わせて設定してください。
<pre>
FREQ_HIGH_BASE = 844.16  # high tone frequency
FREQ_LOW_BASE = 680.02   # low tone frequency
</pre>
<pre>
# 振幅設定
AMP_MAX = 0.025
AMP_MIN = 0.02
</pre>
* 別の雑音が大きい場合は、バンドパスフィルタで制御可能です。
* 不要な場合はコメントアウトをお願いします。
<pre>
# フィルタ係数
FPASS1 = np.array([670, 860]) # 通過域端周波数
FSTOP1 = np.array([600, 950]) # 阻止域端周波数
FPASS2 = np.array([835, 860]) # 通過域端周波数
FSTOP2 = np.array([750, 950]) # 阻止域端周波数
GPASS = 6   # 通過域端最大損失
GSTOP = 30  # 通過域端最小損失
</pre>
#### 実行方法
* 常時起動させておきます。
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
### trainDelay.py
#### 概要
* 電車の遅延情報がLINEで通知されます。
* dataフォルダを作成し、その配下に[こちら](https://rti-giken.jp/fhc/api/train_tetsudo/)のtrain.tsvを配置してください。実行前のチェックで、路線名が正しいかをチェックしています。
#### 実行方法
* jsonfunc.pyに以下を定義し、ファイルを実行してください。
<pre>
TRAIN_ROUTE = '【train.tsv内の路線名】'
</pre>
<pre>
python3 $HOME/python/trainDelay.py
</pre>
### weather.py
#### 概要
* ~~天気情報をLINEで通知していましたが、[livedoor天気](https://help.livedoor.com/weather/index.html)のサービス終了に伴い、利用できなくなっています。~~ 
* 翌日の天気を取得して、LINEに通知されます（気象庁のAPIが利用できるようになったので、そちらに対応しています）。デフォルトでは埼玉県南部の設定になっています。
#### 実行方法
* jsonfunc.py内のXXに各自の都道府県コードを入力してください。また、AREA_MODEについては対象地域に合わせて、適宜修正してください。DATE_MODE=1は翌日を意味しています。
<pre>
WEATHER_URL = 'https://www.jma.go.jp/bosai/forecast/data/forecast/XX0000.json'
DATE_MODE = 1
AREA_MODE = 1
</pre>
<pre>
python3 $HOME/python/weather.py
</pre>
### gitNews.py
#### 概要
* Yahoo!のページから主要ニュースのタイトルを取得します。
#### 実行方法
* 引数が1ならLINEに通知します。それ以外は通知しません。
<pre>
python3 $HOME/python/getNews.py 1 # LINEに通知する
</pre>
### thermometer.py
#### 概要
* SwitchBotの温度計から温度、湿度、バッテリー情報を取得します。
#### 実行方法
* 引数が1ならLINEに通知します。それ以外は通知しません。
<pre>
python3 $HOME/python/thermometer.py 0 # LINEに通知しない
python3 $HOME/python/thermometer.py 1 # LINEに通知する
</pre>
### homeBridge.py
#### 概要
* ~/.homebridge/config.jsonに記載されているデータを抽出、curlコマンドを実行することで操作を行います。
* 本来はAppleのHomeKitアプリ経由で実行していましたが、外出先から実行できない場合があるので、curlを直接実行するようにしています。
* slackと連携すると便利です。
#### 実行方法
* 常時起動させておきます。
<pre>
sudo vi /etc/systemd/system/homebridge.service
</pre>
<pre>
[Unit]
Description=Homebridge
Wants=network-online.target
After=syslog.target network-online.target

[Service]
ExecStart = homebridge
Type=simple
User=smarthome
Restart=always

[Install]
WantedBy=multi-user.target
</pre>
<pre>
python3 $HOME/python/homebridge.py
</pre>
### thermometer.py
#### 概要
* SwitchBot温湿度計で取得した温度、湿度、バッテリー残量を取得します。
#### 実行方法
* env.pyにSwitchBotのMACアドレスを記載してください。
* 引数が1ならLINEに通知します。それ以外は通知しません。
<pre>
THERMOMETER_MAC=''
</pre>
<pre>
$HOME/python/thermometer.py 0 # LINEに通知しない
$HOME/python/thermometer.py 1 # LINEに通知する
</pre>
### thermoCO2meter.py
#### 概要
* SwitchBot CO2センサーで取得した温度、湿度、二酸化炭素濃度、バッテリー残量を取得します。
#### 実行方法
* env.pyにSwitchBotのMACアドレスを記載してください。
* 引数が1ならLINEに通知します。それ以外は通知しません。
<pre>
THERMO_CO2_MAC=''
</pre>
<pre>
$HOME/python/thermoCO2meter.py 0 # LINEに通知しない
$HOME/python/thermoCO2meter.py 1 # LINEに通知する
</pre>
### calcEnergyPrice.py
#### 概要
* 太陽光発電のモニターの内容から前日の使用量や電気料金を計算して表示します。
* dataフォルダ下にenergyPrice.csvを配置してください。単価は東京電力のスマートライフSがデフォルトで設定されています。
#### 実行方法
python3 $HOME/python/calcEnergyPrice.py
### 共通設定
#### logfunc.py
ログの出力場所を各自の環境に合わせて設定してください。
<pre>
log_dir = os.path.expanduser('~') + '/python/log'
</pre>
#### token.py
subfuncフォルダ下にファイルを作成して、Lineのアクセスコードを記載してください。[LINE Notify](https://notify-bot.line.me/ja/)の機能を使っています。
<pre>
ACCESS_TOKEN = ''
</pre>
## 参考文献
* [ラズベリーパイでインターホンの音を検知する](https://westgate-lab.hatenablog.com/entry/2019/12/25/225422)
* [鉄道遅延情報のjson](https://rti-giken.jp/fhc/api/train_tetsudo/)
* [ラズパイでpython3にopencvを入れたらエラーが出た【対処法】](https://qiita.com/XM03/items/48463fd910470b226f22)
* [HomeKitとRaspberry PiとIRKitで部屋の家電をSiriから音声操作する方法](https://techblog.nhn-techorus.com/archives/725)
* [Hubotを使ってSlackに投稿されたメッセージに応答してシェルスクリプトを実行させる](https://www.virment.com/hubot-slack-execute-shell-script/)
* [RaspberryPiで室温の計測（SwitchBot 温湿度計）](https://www.note65536.com/2020/08/raspberrypiswitchbot.html)
* [スイッチボットCO2センサーの遊び方](https://tsuzureya.net/switchbot-co2-meter-hacks/)
