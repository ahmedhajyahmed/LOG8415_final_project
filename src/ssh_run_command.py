import os
import sys
import time
import paramiko
from pathlib import Path
from paramiko.client import SSHClient
from config import *


def ssh_connect(ssh_client: SSHClient, ec2_instance_public_ipv4_address: str) -> None:
    """
    connect to an EC2 instance through SSH

    :param ssh_client: The SSH client
    :param ec2_instance_public_ipv4_address: The public IPv4 address of the EC2 instance to which we are connecting
    :return: None
    """

    max_attempt = 10
    attempt = 1

    while True:
        try:
            print(f'Establishing an SSH connection to EC2 Instance... \nAttempt: {attempt}')
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            private_key = paramiko.RSAKey.from_private_key_file(SSH_CONFIG_STAND_ALONE['KeyPairFile'])
            ssh_client.connect(
                hostname=ec2_instance_public_ipv4_address,
                username=SSH_CONFIG_STAND_ALONE['EC2UserName'],
                pkey=private_key
            )
        except Exception as e:
            if attempt < max_attempt:
                attempt += 1
                time.sleep(5)  # wait 5s between each attempt.
            else:
                print(e)
                sys.exit(1)
        else:
            print(f"SSH connection successfully established to EC2 instance:\n{ec2_instance_public_ipv4_address}")
            break


def ssh_upload(ssh_client: SSHClient, local_path: str, remote_path: str) -> None:
    """
    upload a file to an EC2 instance through SSH

    :param ssh_client: The SSH client
    :param local_path: The file path to upload from the local machine
    :param remote_path: The file path to which it is uploaded on the EC2 instance
    :return: None
    """

    try:
        print(f'Uploading a file to EC2 Instance...')
        sftp_client = ssh_client.open_sftp()
        sftp_client.put(local_path, remote_path)
    except Exception as e:
        print(e)
        sys.exit(1)
    else:
        sftp_client.close()
        print(f'File successfully uploaded to EC2 instance:\n{Path(local_path).name}')


def ssh_run_stand_alone(ec2_instance_public_ipv4_address: str) -> None:
    """
    connect to an EC2 instance, install sql stand alone, and run the setup script on it via SSH

    :param ec2_instance_public_ipv4_address: The public IPv4 address of the EC2 instance to which we are connecting
    :return: None
    """
    ssh_client = paramiko.SSHClient()

    ssh_connect(ssh_client, ec2_instance_public_ipv4_address)

    for local_path in SSH_CONFIG_STAND_ALONE['FilesToUpload']:
        remote_path = str(SSH_CONFIG_STAND_ALONE['RemoteDirectory'] + "/" + Path(local_path).name)
        ssh_upload(ssh_client, os.path.join("uploaded_files", local_path), remote_path)

    _, stdout, stderr = ssh_client.exec_command(
        f"chmod +x {SSH_CONFIG_STAND_ALONE['ScriptToExecute']} && bash {SSH_CONFIG_STAND_ALONE['ScriptToExecute']}",
        get_pty=True
    )

    for line in iter(stdout.readline, ""):
        print(line, end="")


def ssh_run_node_manager(ec2_instance_public_ipv4_address: str, ec2_instances_dns_name: [str]) -> None:
    """
    connect to an EC2 instance, configure the node manager, and run the setup script on it via SSH

    :param ec2_instances_dns_name:
    :param ec2_instance_public_ipv4_address: The public IPv4 address of the EC2 instance to which we are connecting
    :return: None
    """
    ssh_client = paramiko.SSHClient()

    ssh_connect(ssh_client, ec2_instance_public_ipv4_address)

    for local_path in SSH_CONFIG_NODE_MANAGER['FilesToUpload']:
        remote_path = str(SSH_CONFIG_NODE_MANAGER['RemoteDirectory'] + "/" + Path(local_path).name)
        ssh_upload(ssh_client, os.path.join("uploaded_files", local_path), remote_path)

    args = ' '.join(ec2_instances_dns_name)

    _, stdout, stderr = ssh_client.exec_command(
        f"chmod +x {SSH_CONFIG_NODE_MANAGER['ScriptToExecute']} && bash {SSH_CONFIG_NODE_MANAGER['ScriptToExecute']}  "
        f"{args}",
        get_pty=True
    )

    for line in iter(stdout.readline, ""):
        print(line, end="")

    cmd = "sudo /opt/mysqlcluster/home/mysqlc/bin/ndb_mgmd -f /opt/mysqlcluster/deploy/conf/config.ini --initial " \
          "--configdir=/opt/mysqlcluster/deploy/conf/"

    _, stdout, stderr = ssh_client.exec_command(cmd)

    for line in iter(stdout.readline, ""):
        print(line, end="")


def ssh_run_data_nodes(ec2_instance_public_ipv4_address: [str], ec2_instance_dns_name: str) -> None:
    """
    connect to an EC2 instance, configure the data node, and run the setup script on it via SSH

    :param ec2_instance_dns_name:
    :param ec2_instance_public_ipv4_address: The public IPv4 address of the EC2 instance to which we are connecting
    :return: None
    """
    ssh_client = paramiko.SSHClient()

    for ip_adress in ec2_instance_public_ipv4_address:

        ssh_connect(ssh_client, ip_adress)

        for local_path in SSH_CONFIG_DATA_NODE['FilesToUpload']:
            remote_path = str(SSH_CONFIG_DATA_NODE['RemoteDirectory'] + "/" + Path(local_path).name)
            ssh_upload(ssh_client, os.path.join("uploaded_files", local_path), remote_path)

        _, stdout, stderr = ssh_client.exec_command(
            f"chmod +x {SSH_CONFIG_DATA_NODE['ScriptToExecute']} && bash {SSH_CONFIG_DATA_NODE['ScriptToExecute']} "
            f"{ec2_instance_dns_name}",
            get_pty=True
        )

        for line in iter(stdout.readline, ""):
            print(line, end="")

        cmd = "sudo /opt/mysqlcluster/home/mysqlc/bin/ndbd -c " + ec2_instance_dns_name + ":1186"

        _, stdout, stderr = ssh_client.exec_command(cmd)

        for line in iter(stdout.readline, ""):
            print(line, end="")


def ssh_run_sql_node(ec2_instance_public_ipv4_address: str, ec2_instance_dns_name: str) -> None:
    """
    connect to an EC2 instance, configure sql node, and run the setup script on it via SSH

    :param ec2_instance_dns_name:
    :param ec2_instance_public_ipv4_address: The public IPv4 address of the EC2 instance to which we are connecting
    :return: None
    """
    ssh_client = paramiko.SSHClient()

    ssh_connect(ssh_client, ec2_instance_public_ipv4_address)

    for local_path in SSH_CONFIG_SQL_Node['FilesToUpload']:
        remote_path = str(SSH_CONFIG_SQL_Node['RemoteDirectory'] + "/" + Path(local_path).name)
        ssh_upload(ssh_client, os.path.join("uploaded_files", local_path), remote_path)

    _, stdout, stderr = ssh_client.exec_command(
        f"chmod +x {SSH_CONFIG_SQL_Node['ScriptToExecute'][0]} && bash {SSH_CONFIG_SQL_Node['ScriptToExecute'][0]} "
        f"{ec2_instance_dns_name}",
        get_pty=True
    )

    for line in iter(stdout.readline, ""):
        print(line, end="")

    _, stdout, stderr = ssh_client.exec_command(
        f"chmod +x {SSH_CONFIG_SQL_Node['ScriptToExecute'][1]} && bash {SSH_CONFIG_SQL_Node['ScriptToExecute'][1]}",
        get_pty=True
    )

    for line in iter(stdout.readline, ""):
        print(line, end="")


def ssh_run_proxy(ec2_instance_public_ipv4_address: str, ec2_instance_public_ipv4_addresses: [str],
                  mode: str) -> None:
    """
    connect to an EC2 instance, prepare the proxy instance, and run the setup script on it via SSH

    :param mode:
    :param ec2_instance_public_ipv4_addresses:
    :param ec2_instance_public_ipv4_address: The public IPv4 address of the EC2 instance to which we are connecting
    :return: None
    """
    ssh_client = paramiko.SSHClient()

    ssh_connect(ssh_client, ec2_instance_public_ipv4_address)

    for local_path in SSH_CONFIG_PROXY['FilesToUpload']:
        remote_path = str(SSH_CONFIG_PROXY['RemoteDirectory'] + "/" + Path(local_path).name)
        if local_path != "ec2_keypair.pem":
            ssh_upload(ssh_client, os.path.join("uploaded_files", local_path), remote_path)
        else:
            ssh_upload(ssh_client, local_path, remote_path)

    args = ' '.join(ec2_instance_public_ipv4_addresses + [mode])

    _, stdout, stderr = ssh_client.exec_command(
        f"chmod +x {SSH_CONFIG_PROXY['ScriptToExecute']} && bash {SSH_CONFIG_PROXY['ScriptToExecute']}  {args}",
        get_pty=True
    )

    for line in iter(stdout.readline, ""):
        print(line, end="")
