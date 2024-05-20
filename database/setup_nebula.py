import os
from config import nebula_config

def setup_nebula():
    connection_string = f"--address {os.environ['GRAPHD_HOST']} --port 9669 --user root --password {os.environ['NEBULA_PASSWORD']}"
    %reload_ext ngql
    %ngql {connection_string}

    %ngql CREATE SPACE IF NOT EXISTS rag_demo(vid_type=FIXED_STRING(256), partition_num=1, replica_factor=1);

    %ngql USE rag_demo;
    %ngql CREATE TAG IF NOT EXISTS entity(name string);
    %ngql CREATE EDGE IF NOT EXISTS relationship(relationship string);

if __name__ == "__main__":
    setup_nebula()
