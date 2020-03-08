import aria2p
import subprocess
from flask import Flask, render_template, request, redirect, make_response, session,url_for
app = Flask(__name__)

#how to get environment varible values -->  " os.environ['S3_KEY'] "
aria2 = aria2p.API(
        aria2p.Client(
            host="http://localhost",
            port=6800,
            secret=""
        )
    )

@app.route('/run',methods = ['GET'])
def run():
    aria2_daemon_start_cmd = []
    aria2_daemon_start_cmd.append("aria2c")
    aria2_daemon_start_cmd.append("--daemon=true")
    aria2_daemon_start_cmd.append("--enable-rpc")
    aria2_daemon_start_cmd.append("--follow-torrent=mem")
    aria2_daemon_start_cmd.append("--max-connection-per-server=10")
    aria2_daemon_start_cmd.append("--min-split-size=10M")
    aria2_daemon_start_cmd.append("--rpc-listen-all=false")
    aria2_daemon_start_cmd.append("--rpc-listen-port=6800")
    aria2_daemon_start_cmd.append("--rpc-max-request-size=1024M")
    aria2_daemon_start_cmd.append("--seed-ratio=0.0")
    aria2_daemon_start_cmd.append("--seed-time=1")
    aria2_daemon_start_cmd.append("--split=10")
    aria2_daemon_start_cmd.append("--bt-stop-timeout=600")
    subprocess.Popen(aria2_daemon_start_cmd)
    subprocess.call



    downloads = aria2.get_downloads()
    list1=[]
    for download in downloads:
        list1.append(download.name)
        list1.append(download.download_speed)
        list1.append("<br>")
    return str(list1)

@app.route('/',methods = ['GET'])
def home():
    # list downloads
    downloads = aria2.get_downloads()
    list1=[]
    for download in downloads:
        list1.append(download.name)
        list1.append(",")
        list1.append(download.download_speed)
        list1.append("<br>")
    return str(list1)

@app.route('/upload',methods = ['GET'])
def upload():
    return render_template('upload.html')

@app.route('/download',methods = ['GET'])
def download():
    magnet_uri = request.args.get('link')
    gid = aria2.add_magnet(magnet_uri).gid
    new_gid=aria2.get_download(gid).followed_by_ids[0]
    file = aria2.get_download(new_gid)
    list2=[]
    list2.append(str(file.name))
    list2.append(",")
    list2.append(str(file.download_speed_string()))
    list2.append(",")
    list2.append(str(file.upload_speed_string()))
    list2.append(",")
    list2.append(str(file.progress_string()))
    list2.append(",")
    list2.append(str(file.total_length_string()))
    return str(list2)


if __name__ == '__main__':
    app.run(debug=True)
