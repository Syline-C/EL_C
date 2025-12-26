#!/bin/bash

gen_key_mail="example@mail.com"
key_path="$HOME/.ssh"
ssh_category="id_ed25519"

if [ -d "$key_path" ]; then rm -rf "$key_path"; fi

ssh-keygen -t ed25519 -C "$gen_key_mail" -f "$key_path/$ssh_category" -N ""

cat "$key_path/$ssh_category.pub"

chmod 664 "$key_path/$ssh_category.pub"
chmod 600 "$key_path/$ssh_category"
chmod 700 "$key_path"
