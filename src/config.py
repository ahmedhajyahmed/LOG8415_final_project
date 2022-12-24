EC2_CONFIG = {
    'Common': {
        'ServiceName': 'ec2',
        # 'ImageId': 'ami-08c40ec9ead489470',  # Ubuntu, 22.04 LTS, 64-bit (x86)
        'ImageId': 'ami-061dbd1209944525c',  # Ubuntu, 18.04 LTS, 64-bit (x86)
        'KeyPairName': 'log8415_lab1_kp',
        'SecurityGroups': ['log8415_lab1_sg'],
        'InstanceCount': 1,
        'InstanceProfileName': 'LabInstanceProfile',  # We'll use this default role since we can't create a new one.
        'MetadataOptions': {
            'InstanceMetadataTags': 'enabled'
        }
    },
    'Cluster1': {
        'InstanceType': 't2.micro',
        'AvailabilityZone': 'us-east-1a',
        'TagSpecifications': [
            {
                'ResourceType': 'instance',
                'Tags': [
                    {'Key': 'Cluster', 'Value': '1', },
                    {'Key': 'Instance', 'Value': '', }  # Instance tag value is given when creating the instance
                ]
            }
        ]
    },
    'Cluster2': {
        'InstanceType': 't2.large',
        'AvailabilityZone': 'us-east-1a',
        'TagSpecifications': [
            {
                'ResourceType': 'instance',
                'Tags': [
                    {'Key': 'Cluster', 'Value': '2', },
                    {'Key': 'Instance', 'Value': '', }  # Instance tag value is given when creating the instance
                ]
            }
        ]
    }
}

SSH_CONFIG_STAND_ALONE = {
    'EC2UserName': 'ubuntu',
    'KeyPairFile': 'ec2_keypair.pem',
    'FilesToUpload': [
        './benchmark_sql_stand_alone.sh',
    ],
    'RemoteDirectory': '/home/ubuntu/',
    'ScriptToExecute': '/home/ubuntu/benchmark_sql_stand_alone.sh'
}

SSH_CONFIG_NODE_MANAGER = {
    'EC2UserName': 'ubuntu',
    'KeyPairFile': 'ec2_keypair.pem',
    'FilesToUpload': [
        'mysql-cluster-gpl-7.2.1-linux2.6-x86_64.tar.gz',
        'setup_mgm_node.sh',
    ],
    'RemoteDirectory': '/home/ubuntu/',
    'ScriptToExecute': '/home/ubuntu/setup_mgm_node.sh'
}

SSH_CONFIG_DATA_NODE = {
    'EC2UserName': 'ubuntu',
    'KeyPairFile': 'ec2_keypair.pem',
    'FilesToUpload': [
        'mysql-cluster-gpl-7.2.1-linux2.6-x86_64.tar.gz',
        'setup_data_node.sh',
    ],
    'RemoteDirectory': '/home/ubuntu/',
    'ScriptToExecute': '/home/ubuntu/setup_data_node.sh'
}

SSH_CONFIG_SQL_Node = {
    'EC2UserName': 'ubuntu',
    'KeyPairFile': 'ec2_keypair.pem',
    'FilesToUpload': [
        'setup_sql_node.sh',
        'benchmark_sql_cluster.sh',
    ],
    'RemoteDirectory': '/home/ubuntu/',
    'ScriptToExecute': ['/home/ubuntu/setup_sql_node.sh', '/home/ubuntu/benchmark_sql_cluster.sh']
}

SSH_CONFIG_PROXY = {
    'EC2UserName': 'ubuntu',
    'KeyPairFile': 'ec2_keypair.pem',
    'FilesToUpload': [
        'ec2_keypair.pem',
        'proxy.py',
        'proxy.sh',
    ],
    'RemoteDirectory': '/home/ubuntu/',
    'ScriptToExecute': '/home/ubuntu/proxy.sh'
}
