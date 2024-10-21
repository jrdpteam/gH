import sys
import hashlib
import zlib
import os
import argparse
import threading
import time
import magic
from colorama import *
from tqdm import tqdm

init(autoreset=True)

def print_ascii_art():
    ascii_art = f"""
 {Fore.MAGENTA}{Style.BRIGHT}       _    _ 
 {Fore.YELLOW}v3.0{Style.RESET_ALL}{Back.BLUE}{Fore.MAGENTA}{Style.BRIGHT}  | |  | |
   __ _| |__| |
  / _ |  __  |
 | (_| | |  | |
  \__, |_|  |_|
   __/ |{Fore.GREEN}by JRDP{Fore.MAGENTA}{Style.BRIGHT}
  |___/ {Fore.GREEN} Team  {Style.RESET_ALL}
    """
    print(Back.BLUE + ascii_art + Style.RESET_ALL)

def detect_temp_dir():
    if sys.platform.startswith('win'):
        return os.getenv('TEMP', 'C:\\Temp')
    else:
        return os.getenv('TMPDIR', '/tmp')

def read_binary_file(file_path, num_threads=5):
    file_size = os.path.getsize(file_path)
    chunk_size = 1024 * 1024
    data = bytearray(file_size)

    def read_chunk(start, end, progress_bar):
        with open(file_path, 'rb') as file:
            file.seek(start)
            chunk_data = file.read(end - start)
            data[start:end] = chunk_data
            progress_bar.update(end - start)
    
    threads = []
    progress_bar = tqdm(total=file_size, desc="Reading file", unit='B', unit_scale=True)
    for i in range(num_threads):
        start = i * (file_size // num_threads)
        end = (i + 1) * (file_size // num_threads) if i != num_threads - 1 else file_size
        thread = threading.Thread(target=read_chunk, args=(start, end, progress_bar))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    progress_bar.close()
    return data

def calculate_checksums(data):
    checksums = {
        "SHA256": hashlib.sha256(data).hexdigest(),
        "MD5": hashlib.md5(data).hexdigest(),
        "CRC32": format(zlib.crc32(data) & 0xFFFFFFFF, '08X'),
        "Whirlpool": hashlib.new('whirlpool', data).hexdigest(),
    }
    return checksums

def print_checksums(checksums):
    for name, checksum in checksums.items():
        print(f"{name}: {checksum}")

def format_bytes(data, bytes_per_line):
    formatted_data = ''
    count = 0
    formatted_data += '        '
    for byte in data:
        formatted_data += f"0x{byte:02X}, "
        count += 1
        if count % bytes_per_line == 0:
            formatted_data += '\n        '
    return formatted_data.rstrip(', ')

def colorize_byte(byte):
    if byte < 64:
        return f"{Fore.BLUE}0x{byte:02X}{Style.RESET_ALL}"
    elif byte < 128:
        return f"{Fore.GREEN}0x{byte:02X}{Style.RESET_ALL}"
    elif byte < 192:
        return f"{Fore.YELLOW}0x{byte:02X}{Style.RESET_ALL}"
    else:
        return f"{Fore.RED}0x{byte:02X}{Style.RESET_ALL}"

def print_formatted_data(file_path, colorize=False, bytes_per_line=16, display_rate=1500000, show_ascii=False):
    chunk_size = 1024 * 1024
    display_chunk_size = 1024 * 1024
    delay = display_chunk_size / display_rate
    
    with open(file_path, 'rb') as file:
        count = 0
        formatted_data = '        '
        ascii_representation = ''
        start_time = time.time()
        while chunk := file.read(display_chunk_size):
            for i, byte in enumerate(chunk):
                hex_rep = colorize_byte(byte) if colorize else f"0x{byte:02X}"
                formatted_data += f"{hex_rep}, "
                ascii_char = chr(byte) if 32 <= byte <= 126 else '.'
                ascii_representation += ascii_char
                count += 1
                if count % bytes_per_line == 0:
                    formatted_data += '\n        '
                    if show_ascii:
                        formatted_data += f" | {ascii_representation}\n        "
                    ascii_representation = ''
            print(formatted_data.rstrip(', '))
            formatted_data = '        '
            elapsed_time = time.time() - start_time
            if elapsed_time < delay:
                time.sleep(delay - elapsed_time)
            start_time = time.time()

def detect_file_type(file_path):
    file_type = magic.from_file(file_path, mime=True)
    return file_type

def print_stats(data, file_type):
    print(f"File Size: {len(data)} bytes")
    print(f"File Type: {file_type}")
    print(f"Unique Bytes: {len(set(data))}")

def write_data_to_file(file_path, data, bytes_per_line):
    formatted_data = format_bytes(data, bytes_per_line)
    with open(file_path, 'w') as file:
        progress_bar = tqdm(total=len(formatted_data), desc="Writing data", unit='B', unit_scale=True)
        chunk_size = 1024 * 100
        for i in range(0, len(formatted_data), chunk_size):
            file.write(formatted_data[i:i + chunk_size])
            progress_bar.update(len(formatted_data[i:i + chunk_size]))
        progress_bar.close()

def advanced_analysis(data):
    byte_values = np.array(data)
    
    mean = np.mean(byte_values)
    median = np.median(byte_values)
    std_dev = np.std(byte_values)
    entropy = stats.entropy(np.bincount(byte_values) / len(byte_values))
    
    freq, _ = np.histogram(byte_values, bins=range(256))
    skewness = stats.skew(byte_values)
    
    analysis_results = {
        "Mean": mean,
        "Median": median,
        "Standard Deviation": std_dev,
        "Entropy": entropy,
        "Skewness": skewness,
        "Frequency Distribution": freq.tolist()
    }
    
    return analysis_results

def main():
    parser = argparse.ArgumentParser(
        description="gH - tiny bytecode processing framework\nby JRDP Team   https://jrdpteam.netlify.app",
        usage="%(prog)s [options] <file_path>"
    )
    parser.add_argument(
        "file_path", 
        help="Path to the binary file to be processed."
    )
    parser.add_argument(
        "-c", "--colorize", 
        action="store_true", 
        help="Colorize the output for easier reading."
    )
    parser.add_argument(
        "-b", type=int, 
        default=16, 
        help="Number of bytes to display per line (default: 16)."
    )
    parser.add_argument(
        "-t", type=int, 
        default=5, 
        help="Number of threads to use for file loading (default: 5)."
    )
    parser.add_argument(
        "-o", type=str, 
        help="Output file path to write byte data in formatted form."
    )
    parser.add_argument(
        "--ASCII", 
        action="store_true", 
        help="Show ASCII representation of the bytes."
    )
    parser.add_argument(
        "--color-info", 
        action="store_true", 
        help="Show color scale information."
    )
    
    if len(sys.argv) == 1:
        print("Please rerun with -h to learn how to use me >_<")
        sys.exit(0)
    
    args = parser.parse_args()

    if args.color_info:
        print("Color Scale Information:")
        print("0x00 to 0x3F: {}".format(Fore.BLUE + "Light Blue" + Style.RESET_ALL))
        print("0x40 to 0x7F: {}".format(Fore.GREEN + "Light Green" + Style.RESET_ALL))
        print("0x80 to 0xBF: {}".format(Fore.YELLOW + "Light Yellow" + Style.RESET_ALL))
        print("0xC0 to 0xFF: {}".format(Fore.RED + "Light Red" + Style.RESET_ALL))
        sys.exit(0)

    try:
        print_ascii_art()
        binary_data = read_binary_file(args.file_path, num_threads=args.t)
        
        file_type = detect_file_type(args.file_path)
        stats = {
            "File Size": len(binary_data),
            "File Type": file_type,
            "Unique Bytes": len(set(binary_data))
        }
        print_stats(binary_data, file_type)

        checksums = calculate_checksums(binary_data)
        print_checksums(checksums)
        
        if args.o:
            write_data_to_file(args.o, binary_data, args.b)
        else:
            temp_file_path = os.path.join(detect_temp_dir(), 'gH.txt')
            with open(temp_file_path, 'wb') as file:
                file.write(binary_data)
            
            print("\nFormatted Binary Data:\n")
            print_formatted_data(temp_file_path, colorize=args.colorize, bytes_per_line=args.b, show_ascii=args.ASCII)
            
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
                
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
