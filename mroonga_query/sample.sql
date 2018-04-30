#ドリルダウン　出願人
select mroonga_command('select --table publn_data --drilldown applicants --output_columns _applicants,_nsubrecs --query description:@製パン --drilldown_sort_keys -_nsubrecs');

#ドリルダウン FI
select mroonga_command('select --table publn_data --drilldown fi --output_columns _fi,_nsubrecs --query description:@ホームベーカリー --drilldown_sort_keys -_nsubrecs');

#タグ検索
select mroonga_command('select --table publn_data --query fi:@A21D13/ --output_columns publn_nr');

#複数条件 キーワード and
select mroonga_command('select --table publn_data --output_columns publn_nr,applicants,title --match_columns title|claims|description --query " 製パン機 学習"');

#件数取得 limit 0
select mroonga_command('select --table publn_data --output_columns publn_nr,applicants,title --match_columns title|claims|description --query " 製パン機" --limit 0');

#重み付け
select mroonga_command('select --table publn_data --output_columns publn_nr,applicants,title,_score --match_columns "claims * 4 || description" --query " 製パン機" --limit 50 --sort_keys -_score');

#キーワード論理和
select mroonga_command('select --table publn_data --output_columns publn_nr,applicants,title,_score --match_columns "claims * 4 || description" --query " 製パン機 OR ホームベーカリー" --limit 50 --sort_keys -_score');

#フィルタ関数
select mroonga_command('select --table publn_data --output_columns publn_nr,applicants --filter "(description @ \'製パン機 || ホームベーカリー\')" --limit 50');

#条件　複合
select mroonga_command('select --table publn_data --output_columns publn_nr,applicants --match_columns applicants --query "象印マホービン株式会社 OR パナソニック株式会社" --filter "claims @ \'製パン\' || claims @ \'ホームベーカリー\'" --limit 100');

#in values
select mroonga_command('select --table publn_data --output_columns publn_nr,applicants --filter \'in_values(fi,\"H04N1/00,108M\")\' --limit 100');
