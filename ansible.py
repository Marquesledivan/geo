### Import Key Pair to Java Keystore

cat myhost.pem intermediate.pem root.pem > import.pem
openssl pkcs12 -export -in import.pem -inkey myhost.key.pem -name shared > server.p12
keytool -importkeystore -srckeystore server.p12 -destkeystore store.keys -srcstoretype pkcs12 -alias shared

### Delete a certificate from a keystore with keytool
keytool -list -v -keystore keystoreCopy.jks
keytool -delete -alias aliasARetirer -keystore copieKeystore.jks

## Import the Certificate as a Trusted Certificate
keytool -import -alias susan -file Example.cer -keystore exampleraystore
keytool -printcert -file Example.cer


kill -9 `lsof -t  -u postfix`
lsof -l -u postfix
lsof +D /var/log/
lsof -t /var/log/httpd/access_log
lsof -i 4 -a  -p 1633
lsof /var/log | grep -i "deleted"

fuser -k /dev/pts/0

ipcs -s | -wc -l 
cat /proc/sys/kernel/msgmni
cat /proc/sys/kernel/sem
ipcs -s | awk -v user=apache '$3==user {system("ipcrm -s "$2)}'
ipcrm -a

#### LVM
dmsetup info /dev/dm-0
lvdisplay|awk  '/LV Name/{n=$3} /Block device/{d=$3; sub(".*:","dm-",d); print d,n;}'
lsblk --output NAME,KNAME,TYPE,SIZE,MOUNTPOINT
iostat -x -d 1


https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/5/html/tuning_and_optimizing_red_hat_enterprise_linux_for_oracle_9i_and_10g_databases/sect-oracle_9i_and_10g_tuning_guide-setting_semaphores-setting_semaphore_parameters
https://serverfault.com/questions/991946/no-space-left-on-device-ah00023-couldnt-create-the-mpm-accept-mutex-when-re

ipcs -u
ipcs -a
ipcs -q
ipcs -s
ipcs -m -i 425984

# ansible.builtin.shell
ansible linux -i inventory -m shell -a 'systemctl start httpd' -u ledivan --ask-pass -b -K

# ansible.builtin.service
ansible linux -i inventory -m service -a "name=httpd state=restarted" -u ledivan --ask-pass -b -K

# ansible.builtin.copy
ansible linux -i inventory -m copy -a 'src=/Users/ledivan/temp/inventory dest=/root owner=root mode=0644' -u ledivan --ask-pass -b -K

cat inventory
[linux]
192.168.1.53
192.168.1.20

~/.ansible.cfg
[defaults]
ansible_python_interpreter=/usr/bin/python3
inventory = /Users/ledivan/temp/inventory
##vault_password_file = ~/.ansible/vault/password.txt
remote_user = ledivan
##ask_sudo_pass = True
ask_pass      = True
deprecation_warnings = False
command_warnings = False
host_key_checking = False
remote_port = 22

[privilege_escalation]
become=True
become_method=sudo
become_ask_pass=False

# ansible.builtin.service
ansible linux -m service -a "name=httpd state=restarted"  -K

# main.yml

###### Restart Service ########
---
- name: Restart agent
  hosts: all
  become: yes
  tasks:
###### Copy CA ######
  - name: Copy CA
    copy:
      src: hots
      dest: /root/
      owner: ledivan
      group: ledivan
      mode: '0644'
###### Restart agent ######
  - name: Restart agent
    service:
      name: httpd
      enabled: true
      state: restarted

# ansible-playbook
ansible-playbook -i inventory main.yml -K
