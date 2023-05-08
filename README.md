# DNS Manager For ArvanCloud

This is a simple python script to change the ip of your domains in ArvanCloud DNS Manager.

## Installation

```bash
pip install arvan-dns
```

## Usage

### create a text file with your domains

```txt
example.com
example.ir
example.net
```

### run the command

```bash
arvan-dns --email=<your email> --password=your password> --old_ip=<your old ip> --new_ip=<your new ip> --port=<your new port> --domains_file=<your domains file>
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
