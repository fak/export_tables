"""Script:  exporter.py

Export mapping of Pfam-A domains and create a versioned backup of the pfam_maps table eg.: $> python loader.py chembl_15 0_1


--------------------
Author:
Felix Kruger
fkrueger@ebi.ac.uk

"""
import os
import queryDevice
import yaml



def retrieve_acts(params):
    """Run a query for chembl_id, canonical_smiles, molformula.

    Inputs:
    params -- dictionary holding details of the connection string

    """
    acts = queryDevice.queryDevice("SELECT md.chembl_id, cs.canonical_smiles, cs.molformula from molecule_dictionary md JOIN compound_structures cs ON md.molregno = cs.molregno" ,params['release'], params['user'], params['pword'], params['host'], params['port'])
    return acts


def write_table(acts, path):
    """ Export the manual mappings into a molformulas table.

    Input:
    acts -- results of the query
    path -- a filepath to the output file

    """
    out = open(path, 'w')
    out.write("""chembl_id\tcanonical_smiles\tmolformula\n""")
    for act in acts:
        chembl_id = act[0]
        canonical_smiles = act[1]
        molformula = act[2]
        out.write("""%(chembl_id)i\t%(canonical_smiles)i\t%(molformula)i\n"""%locals())
    out.close()




def exporter():
    """Main function to export molformulas."""
    # Read config file.
    param_file = open('local.yaml')
    params = yaml.safe_load(param_file)
    param_file.close()

    # Get activities for domains.
    acts  = retrieve_acts(params)

    # Write activity on new manual_pfam_maps file
    path = 'data/molformulas_%(release)s.tab' %params
    write_table(acts, path)


if __name__ == '__main__':
    import sys
    if len(sys.argv) != 1:  # the program name and the two arguments
        sys.exit("All parameters are specified in local.yaml or example.yaml, depending on line 173+174 ")

    exporter()
