import subprocess
from pathlib import Path
from time import time, strftime, gmtime, ctime
import pandas as pd
import numpy as np
from utilities import text_color, create_folder, show_time
import io
import sys

__author__ = "Johnathan Lin <jagonball@g-mail.nsysu.edu.tw>"
__email__ = "jagonball@g-mail.nsysu.edu.tw"


def main():
    time_start = time()
    print(f"ncbi_data.py start time: {ctime(time_start)}")

    input_file = Path("D:/Repositories/25_01_Liver_Cancer/data/Microarray_Huh7_normalized.txt")
    input_colname = "GeneName"

    output_folder = Path("D:/Repositories/25_01_Liver_Cancer/analysis/")
    # Get gene metadata by NCBI gene ID, gene symbol or RefSeq accession.
    input_type = "symbol"  # "gene-id" "accession" "taxon"
    # Collect GO terms from 
    # 1. "all": all returned results.
    # 2. "strict": only from the identical gene symbol.
    match_method = "strict"  # "all" or "strict"
    
    
    df = pd.read_table(input_file, sep='\t')
    print(f"The shape of df: {df.shape}")
    # print(df)

    df_test = df.iloc[8:10, :]
    print(f"The shape of df_test: {df_test.shape}")
    
    # gene_list = ["WIPI2", "KIAA1549L", "ZG16B"]
    gene_list = df_test[input_colname]
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
    
    
    for i, row in df_test.iterrows():
        # print(i)
        # print(row)
        gene = row[input_colname]
        print(gene)
        # df_test.loc[i, "test"] = f'test{i}'

        dataset_command = ["datasets", "summary", "gene", input_type]
        dataset_command.append(gene)
        command = dataset_command + fields_command

        ## Run the command and pass result to a DataFrame.
        # Execute the command and capture the output.
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        # print(type(result.stdout))
        # Check for errors.
        if result.returncode != 0:
            print("Error:", result.stderr)
        else:
            if result.stdout != "":
                # Convert the tsv output to a Pandas DataFrame.
                df_gene = pd.read_csv(io.StringIO(result.stdout), sep="\t")

                # Display the DataFrame.
                print(df_gene)
                # # Write to file.
                # output_file = output_folder / "test_gene" / f"{gene}.txt"
                # df_gene.to_csv(output_file, sep='\t', index=False)


                ## Check if there are multiple symbols.
                if match_method == "strict":
                    list_symbol = df_gene["Symbol"].unique()
                    print(list_symbol)
                    if len(list_symbol) > 1:
                        print(f"{gene} has more than 1 match: {list_symbol}")
                    print(df_gene.shape)
                    df_gene = df_gene[df_gene["Symbol"] == gene]
                    print(df_gene.shape)
                elif match_method == "all":
                    pass
                else:
                    print(f'Error: please check "match_method".')
                    sys.exit()

                # ## Manage GO term.
                # dict_go = {"Gene Ontology Biological Process Go ID": "GOBP_ID",
                #            "Gene Ontology Biological Process Name": "GOBP_NAME",
                #            "Gene Ontology Cellular Component Go ID": "GOCC_ID",
                #            "Gene Ontology Cellular Component Name": "GOCC_NAME",
                #            "Gene Ontology Molecular Function Go ID": "GOMF_ID",
                #            "Gene Ontology Molecular Function Name": "GOMF_NAME"}

                # for col in dict_go:
                #     unique_terms = df_gene[col].unique()
                #     # print(unique_terms)
                #     terms = ""
                #     if not len(unique_terms) == 1:
                #         terms = ';'.join(unique_terms)
                #     else:
                #         ## If there's no matching term, the array is [nan] with dtype "float64".
                #         if not unique_terms.dtype=="float64":
                #             terms = unique_terms[0]
                #     # print(dict_go[col])
                #     # print(terms)
                #     df_test.loc[i, dict_go[col]] = terms

    # print(df_test)
    # output_file = output_folder / f"test_result.txt"
    # df_test.to_csv(output_file, sep='\t', index=False)


    # ## Single gene test.
    # dataset_command = ["datasets", "summary", "gene", input_type]
    # dataset_command.append("CTSO")
    # command = dataset_command + fields_command
    # ## Run the command and pass result to a DataFrame.
    # # Execute the command and capture the output.
    # result = subprocess.run(command, shell=True, capture_output=True, text=True)
    # # print(type(result.stdout))
    # # Check for errors.
    # if result.returncode != 0:
    #     print("Error:", result.stderr)
    # else:
    #     if result.stdout != "":
    #         # Convert the tsv output to a Pandas DataFrame.
    #         df_gene = pd.read_csv(io.StringIO(result.stdout), sep="\t")

    #         # Display the DataFrame.
    #         print(df_gene)


    time_end = time()
    time_used = time_end - time_start
    show_time(time_used, "Total timme taken")


if __name__=="__main__": 
    main()