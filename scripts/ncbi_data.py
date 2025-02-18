import subprocess
from pathlib import Path
from time import time, strftime, gmtime, ctime
import pandas as pd
from utilities import text_color, create_folder, show_time
import io

__author__ = "Johnathan Lin <jagonball@g-mail.nsysu.edu.tw>"
__email__ = "jagonball@g-mail.nsysu.edu.tw"


def main():
    time_start = time()
    print(f"ncbi_data.py start time: {ctime(time_start)}")

    output_file = Path("D:/Repositories/25_01_Liver_Cancer/analysis/test_result.txt")

    dataset_command = ["datasets", "summary", "gene", "symbol"]
    gene_list = ["WIPI2"]#, "KIAA1549L", "ZG16B"]
    ## Showing fields please refer to: https://www.ncbi.nlm.nih.gov/datasets/docs/v2/command-line-tools/using-dataformat/gene-data-reports/
    fields_command = ["--taxon",
                      "human",
                     "--as-json-lines",
                     "|",
                     "dataformat",
                     "tsv",
                     "gene", 
                     "--fields",
                     "symbol,gene-id,synonyms,description,ensembl-geneids,gene-type,\
                     go-bp-id,go-bp-name,\
                     go-cc-id,go-cc-name,\
                     go-mf-id,go-mf-name,\
                     name-id,orientation,transcript-count,protein-count"]
    command = dataset_command + gene_list + fields_command

    # ## Run the command and print the output
    # output = subprocess.run(command,
    #                         shell=True,
    #                         stdout=subprocess.PIPE,
    #                         stderr=subprocess.PIPE)
    # print(output.stdout.decode("utf-8"))


    # ## Run the command and save the output to file.
    # with open(output_file, "w") as f:
    #     subprocess.run(command, shell=True, stdout=f)

    
    ## Run the command and pass to a DataFrame.
    # Execute the command and capture the output.
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    # Check for errors.
    if result.returncode != 0:
        print("Error:", result.stderr)
    else:
        # Convert the tsv output to a Pandas DataFrame.
        df = pd.read_csv(io.StringIO(result.stdout), sep="\t")

        # Display the DataFrame.
        print(df)
        # Write to file.
        df.to_csv(output_file, sep='\t', index=False)


    time_end = time()
    time_used = time_end - time_start
    show_time(time_used, "Total timme taken")


if __name__=="__main__": 
    main()