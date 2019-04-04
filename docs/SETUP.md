# Freeswitch setup

Since I don't run Windows servers, I won't be providing a windows-friendly setup here. Sorry.

### Ubuntu Setup:

##### Install the prerequisites.

``` bash
  sudo apt update
  sudo apt install build-essential autoconf cmake yasm \
  python2 python2-dev libtool-bin git libjpeg-dev libsqlite3-dev \
  libcurl4-openssl-dev libspeex-dev libspeexdsp-dev libedit-dev \
  libtiff-dev libsndfile1-dev -y
```
##### Now grab and build freeswitch:

``` bash
  git clone https://freeswitch.org/stash/scm/fs/freeswitch.git
  cd freeswitch
  ./bootstrap.sh

```  

##### Edit modules.conf

change:
  - ```#languages/mod_python```  to   ```languages/mod_python ```

Also change:
  - ```mod_enum``` to ```#mod_enum```
  - ```mod_opus``` to ```#mod_opus```
  - ```languages/mod_lua```  to   ```#languages/mod_lua```

##### Now run...

``` bash
  ./configure
```
and watch for additional required libraries you may need to install if the build script has changed since this was written.

Once that's done, run:
``` bash
make && sudo make install
```
This will build freeswitch, and then attempt to install if it succeeds.


Files will be installed in ```/usr/local/freeswitch``` by default.


### Configuration


Edit : /usr/local/freeswitch/conf/dialplan/public/00_inbound.xml

Replace the contents with this:
``` xml
<include>
  <extension name="public_did">
  <condition field="destination_number" expression="^(.*)$">
    <action application="set“ data="domain_name=$${domain}"/>
    <action application="python" data=“proxy"/>
  </condition>
  </extension>
</include>

```

Edit : /usr/local/freeswitch/conf/sip_profiles/internal/alcazarnetworks.xml

Add this content:
``` xml
<include>
  <gateway name="alcazar_east2">
    <param name="username" value=“YOUR_USER_NAME" />
    <param name="liberal-dtmf" value="true"/>
    <param name="password" value=“YOUR_ALCAZAR_GATEWAY_PASSWORD" />
    <param name="from-user" value="YOUR_USER_NAME" />
    <param name="proxy" value="162.212.218.52" />
    <param name="register-proxy" value="162.212.218.52:5060" />
    <param name="realmx" value="alcazarnetworks.com" />
    <param name="caller-id-in-from" value="true"/>
    <param name="register" value="false" />
    <param name="rtp-ip" value="${local_ip_v4}"/>
    <param name="sip-ip" value="${local_ip_v4}"/>
    <param name="ext-rtp-ip" value="auto-nat"/>
    <param name="ext-sip-ip" value="auto-nat"/>
    </gateway>
</include>
```


If you want to do outbound calling, you'll need to do this:

Edit : /usr/local/freeswitch/conf/sip_profiles/external/alcazarnetworks.xml

``` xml
<include>
  <gateway name="alcazar_out">
    <param name="username" value=“YOUR_ALCAZAR_USERNAME" />
    <param name="password" value=“YOUR_ALCAZAR_GATEWAY_PASSWORD" />
    <param name="proxy" value="162.212.218.11" />
    <param name="realm" value="162.212.218.11" />
    <param name="caller-id-in-from" value="true"/>
    <param name="domain" value="$${domain}"/>
    <param name="interval" value="10"/>
    <param name="ping" value="25"/>
    <param name="dtmf-mode" value="rfc2833" />
    <param name="from-user" value=" YOUR_ALCAZAR_USERNAME " />
    <param name="caller-id-name" value="$${outbound_caller_name}"/>
    <param name="caller-id-number" value="$${outbound_caller_id}"/>
    <param name="caller-controls" value="plain"/>
    <param name="comfort-noise" value="true"/>
  </gateway>
</include>
```

##### Now allow alcazar through the Freeswitch firewall.

Edit : /usr/local/freeswitch/conf/autoload_configs/acl.conf

Change ```<network-lists></network-lists>``` to look like this:

``` xml
<network-lists>
  <list name="domains" default="deny">
    <node type="allow" domain="$${domain}"/>
    <node type="allow" cidr="162.212.218.50/32" />
    <node type="allow" cidr="162.212.218.52/32" />
  </list>
</network-lists>
```

##### Now add the proxy starter and restart freeswitch

```
cd /usr/local/freeswitch/scripts
git clone https://github.com/hipcast/freeswitch-python.git easy
find . -type d -exec chmod 775 {} \;
find . -type f -name "*py" -exec chmod 554 {} \;
systemctl restart freeswitch
```

##### Your freeswitch server is ready to accept calls.


##### To configure Alcazar, you'll need to:

  - Open an account:
    - go to [AlcazarNetworks.com](https://www.alcazarnetworks.com/signup1.php)
  - Open your firewall/iptables to the Alcazar IP addresses you placed in /usr/local/freeswitch/conf/autoload_configs/acl.conf
    - UDP 5060/5061 Inbound for SIP
    - UDP 5080/5081 Outbound for SIP
    - UDP/TCP 16384-32768 Inbound/Outbound for Media Channels
  - Ensure requests are passing both directions

##### Once your account with Alcazar is active, you can use the promo code when ordering numbers:

- Use Promo Code : VSFREE5-31-19 to get
  - Flat rate inbound toll-free @ $0.0109/min (1/2 price of Twilio)
  - $0.25/mo per Toll-Free number
  - Free Toll-Free # porting
  - Free New Toll-Free number setup
  - Free Local number porting and setup
  - Inbound call termination at $0.001/min no min/max
  - **Disclaimer** : *Nobody* receives any commissions, fees, or credits for using this code. The benefit is entirely for the customer.


![Alcazar Promo Info](alcazarpromo.png)
