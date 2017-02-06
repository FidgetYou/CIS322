curl https://classes.cs.uoregon.edu//17W/cis322/files/osnap_legacy.tar.gz > legacy.tar.gz

tar -xzf legacy.tar.gz

python3 snapped.py $1 5432 product_list.csv products vendor 5 products description 0 products alt_description 2

python3 snapped.py $1 5432 MB005_inventory.csv assets asset_tag 0 assets description 1

python3 snapped.py $1 5432 NC_inventory.csv assets asset_tag 0 assets description 1

python3 snapped.py $1 5432 SPNV_inventory.csv assets asset_tag 0 assets description 1

python3 snapped.py $1 5432 HQ_inventory.csv assets asset_tag 0 assets description 1

python3 snapped.py $1 5432 DC_inventory.csv assets asset_tag 0 assets description 1

python3 snapped.py $1 5432 convoy.csv convoys request 0 convoys depart_dt 1 convoys arrive_dt 6

python3 snapped.py $1 5432 security_levels.csv levels abbrv 0 levels comment 1

python3 snapped.py $1 5432 security_compartments.csv compartments abbrv 0 compartments comment 1

