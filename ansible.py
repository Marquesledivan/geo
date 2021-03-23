ansible linux -i inventory -m ansible.builtin.shell -a 'systemctl start httpd' -u ledivan --ask-pass -b -K

ansible linux -i inventory -m ansible.builtin.service -a "name=httpd state=restarted" -u ledivan --ask-pass -b -K

ansible linux -i inventory -m copy -a 'src=/Users/ledivan/temp/inventory dest=/root owner=root mode=0644' -u ledivan --ask-pass -b -K

cat inventory

[linux]
192.168.1.53
192.168.1.20
