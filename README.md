# LOG8415_final_project
Final Lab Assignment of LOG8415: Scaling Databases and Implementing Cloud Patterns

## Run the program with default credentials

    main.py -m [-h] [-r] {aws} ...

### required arguments:
    -m, --mode   the type of the proxy implementation: direct, random or custom

### optional arguments:

    -h, --help   show this help message and exit
    -r, --reset  reset user's aws account.

## Run the program with manually entered credentials

### aws arguments:

    {aws}
    
    usage: python3.9 main.py aws [-h] -g AWS_REGION_NAME -i AWS_ACCESS_KEY_ID -s AWS_SECRET_ACCESS_KEY -t AWS_SESSION_TOKEN

### optional arguments:

    -h,                         --help                              show this help message and exit
    -g AWS_REGION_NAME,         --region    AWS_REGION_NAME         region name for your AWS account.
    -i AWS_ACCESS_KEY_ID,       --id        AWS_ACCESS_KEY_ID       access key for your AWS account.
    -s AWS_SECRET_ACCESS_KEY,   --secret    AWS_SECRET_ACCESS_KEY   secret key for your AWS account.
    -t AWS_SESSION_TOKEN,       --token     AWS_SESSION_TOKEN       session key for your AWS account.
