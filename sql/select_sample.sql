select appln_nr,publn_nr,title from publn_data where match(applicants) against('+パナソニック' in boolean mode)

select applicants from publn_data where match(applicants) against('+パナソニック' in boolean mode)
