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
