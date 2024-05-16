import paramiko

def exec(cmd):
    # 设置远程服务器的IP地址、用户名和密码
    hostname = '192.168.1.167'
    username = 'root'
    # password = '666666WW'
    private_key_path = '/Users/mac01/.ssh/id_rsa'

    # 创建SSH客户端对象
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # 加载私钥文件
    private_key = paramiko.RSAKey.from_private_key_file(private_key_path)

    # 连接到远程服务器
    ssh.connect(hostname, username=username, pkey=private_key)

    # 执行命令
    stdin, stdout, stderr = ssh.exec_command(cmd)

    # 读取命令输出
    output = stdout.read().decode()

    # 关闭SSH连接
    ssh.close()
    return output

if __name__ == '__main__':
    exec('ls -lh')