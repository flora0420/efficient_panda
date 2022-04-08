# Efficient Pandas
a mini project to showcase efficient ways to iterating over rows in a Pandas DataFrame [Original Medium Post](https://medium.com/towards-data-science/efficiently-iterating-over-rows-in-a-pandas-dataframe-7dd5f9992c01) in [streamlit](https://streamlit.io), deployed on AWS EC2, following [this tutorial](https://towardsdatascience.com/how-to-deploy-a-streamlit-app-using-an-amazon-free-ec2-instance-416a41f69dc3).

## Launch
### Local
```bash
git clone https://github.com/flora0420/efficient_panda
cd efficient_panda
pip install -r requirements.txt
streamlit run src/app.py
```
or one can save `streamlit run src/app.py` to a file, say named `run-ep.sh`, run `chmod 755 run-ep.sh` and then run `./run-ep.sh` to launch the app. 

### Directly from Github
```bash
streamlit run https://raw.githubusercontent.com/flora0420/efficient_panda/main/src/app.py
```
### Deployment using EC2
Once the app works (tested) well both locally and from Github, we are ready to host it on AWS EC2. 

EC2 offers 750 hours of Linux and Windows `t2.micro` instances each month for one year, for this project we will use `t2.micro` instances.

- AMI Selection. I selected 20.04 Ubuntu Server for Amazon Machine Image (AMI) since it's faster to install than 18.04. But if one has more AWS-related work, choose Amazon Linux 2. Both are free-tier eligible. 

- Instance Type Selection. I selected `t2.micro` that is elibile for the free tier. One single CPU instance with 1GB of RAM is enough for this project.

- Keep pressing `Next` until Step 6. Configure Security Group, follow the tutorial to add Custom TCP Rule. 

- Create a new key pair and save it `streamlit-ec2.pem` to your local machine. For Linux AMIs, the private key file allows you to securely SSH into the instance.

- Launch the EC2 instance. It took ~ 30 seconds before the status changed to `running` from `pending`.

- SSH into the instance. [Trouble shooting reference if running into any trouble](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/TroubleshootingInstancesConnecting.html#TroubleshootingInstancesCommonCauses). In my case, I missed the inbound rule for ssh, so I stopped the instance, added the rule and restarted the instance, note that the public DNS(IPv) address changes after restarting.

- install requirements.
    ```bash
    # install miniconda and add its path to env
    sudo apt-get update
    wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh
    bash ~/miniconda.sh -b -p ~/miniconda
    echo "PATH=$PATH:$HOME/miniconda/bin" >> ~/.bashrc
    source ~/.bashrc

    # install streamlit
    pip install streamlit
    pip install matplotlib

    # tmux to avoid ssh timeout
    sudo apt-get install tmux
    tmux new -s StreamlitSession
    ```
- Get code from Github.
```bash
git clone https://github.com/flora0420/efficient_panda.git

cd efficient_panda/
streamlit run src/app.py
```

SUCCESS! The app is online: http://34.212.121.16:8501

- Final step: detach tmux session so that it continues running in the background when you leave ssh shell. Press Ctrl+b and d.  (later attach tmux session `tmux attach -t StreamlitSession`)


### Deployment using Beanstalk
The [HOWTOs using Elastic Beanstalk and Docker](https://discuss.streamlit.io/t/howto-streamlit-on-aws-with-elastic-beanstalk-and-docker/10353) requires a bit of setup with Docker. The official [doc](https://aws.amazon.com/elasticbeanstalk/) suggests it is easy to use, will try later. 