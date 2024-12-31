ip_dest=$1
port_dest=$2
interface_name=$3
port_src=$4
ip_src=$(/sbin/ip -o -4 addr list $interface_name | awk '{print $4}' | cut -d/ -f1)
mac_src=$(ifconfig $interface_name | grep -o -E '([[:xdigit:]]{1,2}:){5}[[:xdigit:]]{1,2}')
mac_gateway=$(arp -a| grep gateway | grep -o -E '([[:xdigit:]]{1,2}:){5}[[:xdigit:]]{1,2}')
# creating the file with this format:
# ip_dest
# port_dest
# ip_src
# port_src
# interface_name
# mac_src
# mac_gateway
echo $ip_dest > ip_dest.txt
echo $port_dest > port_dest.txt
echo $ip_src > ip_src.txt
echo $port_src > port_src.txt
echo $interface_name > interface_name.txt
echo $mac_src > mac_src.txt
echo $mac_gateway > mac_gateway.txt
# replacing ':' with ' ' in mac_src
mac_src_space=$(echo $mac_src | tr ':' ' ')
# replacing ':' with ' ' in mac_gateway
mac_gateway_space=$(echo $mac_gateway | tr ':' ' ')
# echoing these new variables to the file
echo $mac_src_space > mac_src_space.txt
echo $mac_gateway_space > mac_gateway_space.txt
# and saving them in a info1 file
: > info.txt
cat ip_dest.txt >> info.txt
cat port_dest.txt >> info.txt
cat ip_src.txt >> info.txt
cat port_src.txt >> info.txt
cat interface_name.txt >> info.txt
cat mac_src_space.txt >> info.txt
cat mac_gateway_space.txt >> info.txt
