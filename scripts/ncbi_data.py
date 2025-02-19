import subprocess
from pathlib import Path
from time import time, strftime, gmtime, ctime
import pandas as pd
import numpy as np
from utilities import text_color, create_folder, show_time
import io

__author__ = "Johnathan Lin <jagonball@g-mail.nsysu.edu.tw>"
__email__ = "jagonball@g-mail.nsysu.edu.tw"


def main():
    time_start = time()
    print(f"ncbi_data.py start time: {ctime(time_start)}")

    input_file = Path("D:/Repositories/25_01_Liver_Cancer/data/Microarray_Huh7_normalized.txt")
    input_colname = "GeneName"

    output_file = Path("D:/Repositories/25_01_Liver_Cancer/analysis/test_result.txt")
    # Get gene metadata by NCBI gene ID, gene symbol or RefSeq accession.
    input_type = "symbol"  # "gene-id" "accession" "taxon"
    
    
    df = pd.read_table(input_file, sep='\t')
    print(df.shape)

    df_test = df.iloc[0:20, :]
    print(df_test.shape)
    
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
        print(i)
        # print(row)
        gene = row[input_colname]
        df_test.loc[i, "test"] = f'test{i}'

        dataset_command = ["datasets", "summary", "gene", input_type]
        dataset_command.append(gene)
        command = dataset_command + fields_command

    #     ## Run the command and pass result to a DataFrame.
    #     # Execute the command and capture the output.
    #     result = subprocess.run(command, shell=True, capture_output=True, text=True)
    #     # print(type(result.stdout))
    #     # Check for errors.
    #     if result.returncode != 0:
    #         print("Error:", result.stderr)
    #     else:
    #         if result.stdout != "":
    #             # Convert the tsv output to a Pandas DataFrame.
    #             df_gene = pd.read_csv(io.StringIO(result.stdout), sep="\t")

    #             # # Display the DataFrame.
    #             # print(df_gene)
    #             # # Write to file.
    #             # df_gene.to_csv(output_file, sep='\t', index=False)


    #             ## Check if there are multiple symbols.
    #             list_symbol = df_gene["Symbol"].unique()
    #             print(list_symbol)
    #             if len(list_symbol) > 1:
    #                 print(f"{gene} has more than 1 match: {list_symbol}")


    #             ## Manage GO term.
    #             dict_go = {"Gene Ontology Biological Process Go ID": "GOBP_ID",
    #                        "Gene Ontology Biological Process Name": "GOBP_NAME",
    #                        "Gene Ontology Cellular Component Go ID": "GOCC_ID",
    #                        "Gene Ontology Cellular Component Name": "GOCC_NAME",
    #                        "Gene Ontology Molecular Function Go ID": "GOMF_ID",
    #                        "Gene Ontology Molecular Function Name": "GOMF_NAME"}

    #             for col in dict_go:
    #                 unique_terms = df_gene[col].unique()
    #                 # print(unique_terms)
    #                 terms = ""
    #                 if not len(unique_terms) == 1:
    #                     terms = ';'.join(unique_terms)
    #                 else:
    #                     ## If there's no matching term, the array is [nan] with dtype "float64".
    #                     if not unique_terms.dtype=="float64":
    #                         terms = unique_terms[0]
    #                 # print(dict_go[col])
    #                 # print(terms)
    #                 df_test.loc[gene, dict_go[col]] = terms

    print(df_test)
    # df_test.to_csv(output_file, sep='\t', index=False)

    time_end = time()
    time_used = time_end - time_start
    show_time(time_used, "Total timme taken")


if __name__=="__main__": 
    main()