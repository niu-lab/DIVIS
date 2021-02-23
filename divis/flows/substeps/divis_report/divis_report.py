from HTMLTable import HTMLTable
import pandas as pd
import html
import json
import re

'''
 file path
'''
raw_QC_path = "./data/CNIC-02-04-0032-01-WES-PP-4201.fastp.json"
align_QC_path = "./data/genome_results.txt"
calling_QC_path = "./data/mutation_of_callers.txt"

annotation_stat_path = './data/annotationStat.hexy.20210108.v1.xlsx'
gene_number_path = './data/top100gene.xlsx'
chr_num_path ='./data/chrmutdata.xlsx'
'''
read data from file
'''

with open(raw_QC_path, 'r') as load_f:
    raw_QC_dict = json.load(load_f)

align_QC_dict = {}
with open(align_QC_path, 'r') as file:
    data = file.readlines()
    for line in data:
        if ' = ' in line:
            key, value = line.split('=')
            key, value = key.strip(), value.strip() 
            value = value.replace(',', '') 
            align_QC_dict[key] = value
        elif ' >= ' in line:
            value, key = line.split('>=')
            key, value = key.strip(), value.strip()
            value = value.split()[3]
            if '%' in value:
                value = '%.2f%%' % (float(value.strip('%')) / 100 * 100)
            align_QC_dict[key] = value

raw_QC_data = pd.DataFrame({'key': ['raw_reads', 'clean_reads', 'read_length', 'q20', 'q30', 'gc', 'insert_size'],
                            'value': [raw_QC_dict['summary']['before_filtering']['total_reads'],
                                      raw_QC_dict['summary']['after_filtering']['total_reads'], ','.join(
                                    [str(raw_QC_dict['summary']['after_filtering']['read1_mean_length']),
                                     str(raw_QC_dict['summary']['after_filtering']['read2_mean_length'])]),
                                      '%.2f%%' % (raw_QC_dict['summary']['after_filtering']['q20_rate'] * 100),
                                      '%.2f%%' % (raw_QC_dict['summary']['after_filtering']['q30_rate'] * 100),
                                      '%.2f%%' % (raw_QC_dict['summary']['after_filtering']['gc_content'] * 100),
                                      raw_QC_dict['insert_size']['peak']]
                            })

align_QC_data = pd.DataFrame({'key': ['mean_depth', 'depth > 4X', 'depth > 10X', 'depth > 20X', 'depth > 30X',
                                      'depth > 40X', 'depth > 50X', 'mapped reads', 'dup_reads', 'dup_ratio'],
                              'value': [align_QC_dict['mean coverageData'][:-1], align_QC_dict['>= 4X'],
                                        align_QC_dict['>= 10X'], align_QC_dict['>= 20X'], align_QC_dict['>= 30X'],
                                        align_QC_dict['>= 40X'], align_QC_dict['>= 50X'],
                                        re.sub("\(.*\)|\s-\s.*", "", align_QC_dict['number of mapped reads']),
                                        align_QC_dict['number of duplicated reads (estimated)'],
                                        align_QC_dict['duplication rate']]
                              })

calling_QC_data = pd.read_table(calling_QC_path, index_col=None, header=0, sep='\t')

gene_rank_data = pd.read_excel(
    io=gene_number_path,
    index_col=None,
    header=0
)

chr_rank_data = pd.read_excel(
    io=chr_num_path,
    index_col=None,
    header=0
)
tagcloud_data = "[\n";
for i in range(0, len(gene_rank_data)):
    tagcloud_data += "{\"x\": \"" + gene_rank_data.iloc[i]['Gene'].upper()+"\", "+"value: " + str(gene_rank_data.iloc[i]['Value']) + "},\n"
tagcloud_data += "]"

chr_bar_data = "[\n";
for i in range(0, len(chr_rank_data)):
    chr_bar_data += "[\'" + chr_rank_data.iloc[i]['Chr']+"\', " + str(chr_rank_data.iloc[i]['Indels']) + ", " + str(chr_rank_data.iloc[i]['SNPs']) + "],\n"
chr_bar_data += "]\n"

'''
html content
'''
# table and its title (caption)
raw_QC_html_table = HTMLTable()

# table headers
raw_QC_html_table.append_header_rows((
    ('Quality control of raw sequencing data', ' ', ' '),
))

# table content
for i in range(0, len(raw_QC_data)):
    raw_QC_html_table.append_data_rows((
        (
            html.unescape(str(
                'DIVIS processes raw sequencing data with <a href="http://www.bioinformatics.babraham.ac.uk/projects/fastqc/">FasfQC</a> and <a href = "https://github.com/OpenGene/fastp">Fastp</a>')),
            str(raw_QC_data.iloc[i]['key']),
            str(raw_QC_data.iloc[i]['value']),
        ),
    ))

# merge table lines
raw_QC_html_table[0][0].attr.colspan = 3
raw_QC_html_table[1][0].attr.rowspan = 7

align_QC_html_table = HTMLTable()
align_QC_html_table.append_header_rows((
    ('Quality control of alignment data ', ' ', ' '),
))

for j in range(0, len(align_QC_data)):
    align_QC_html_table.append_data_rows((
        (
        'DIVIS maps clean sequencing reads with <a href="https://github.com/lh3/bwa">BWA</a>, sorts and deduplicates the raw alignment with <a href="https://github.com/broadinstitute/picard/">Picard</a>, then perform '
        'the realignment and BQSR with <a href="https://github.com/broadinstitute/gatk">GATK</a>',
        str(align_QC_data.iloc[j]['key']),
        str(align_QC_data.iloc[j]['value']),
        ),
    ))
align_QC_html_table[0][0].attr.colspan = 3
align_QC_html_table[1][0].attr.rowspan = 10

calling_QC_html_table = HTMLTable()
calling_QC_html_table.append_header_rows((
    ('statistics of variants', ' ', ' ', ' ', ' ', ' ', ' '),
))
calling_QC_html_table.append_header_rows((
    ('Description', 'caller', 'SNVs', 'Insertions', 'Deletions', 'Complexs', 'Ti/Tv'),
))

for j in range(0, len(calling_QC_data)):
    calling_QC_html_table.append_data_rows((
        (
        'DIVIS detected variants with <a href="https://github.com/AstraZeneca-NGS/VarDictJava">VarDict</a>, <a href="https://github.com/dkoboldt/varscan">VarScan</a>, <a href="https://github.com/Illumina/strelka/">Strelka</a> and <a href="https://github.com/genome/pindel">Pindel</a>, then merge SNVs and indels from at least 2 '
        'callers',
        str(calling_QC_data.iloc[j]['caller']),
        str(calling_QC_data.iloc[j]['SNVs']),
        str(calling_QC_data.iloc[j]['Insertions']),
        str(calling_QC_data.iloc[j]['Deletions']),
        str(calling_QC_data.iloc[j]['Complex']),
        str(calling_QC_data.iloc[j]['Ti/Tv']),
        ),
    ))
calling_QC_html_table[0][0].attr.colspan = 7
calling_QC_html_table[2][0].attr.rowspan = 5

# css
# title of table
raw_QC_html_table.caption.set_style({
    'font-size': '15px',
    'font-weight': '700',
    'padding': '3px',
    'margin': 'auto',
})
align_QC_html_table.caption.set_style({
    'font-size': '15px',
    'font-weight': '700',
    'padding': '3px',
    'margin': 'auto',
})

calling_QC_html_table.caption.set_style({
    'font-size': '15px',
    'font-weight': '700',
    'padding': '3px',
    'margin': 'auto',
})

raw_QC_html_table.set_style({
    'border-collapse': 'collapse',
    'word-break': 'hyphenate',
    'white-space': 'pre-wrap',
    'width': '60%',
    'margin': 'auto',
})

align_QC_html_table.set_style({
    'border-collapse': 'collapse',
    'word-break': 'hyphenate',
    'white-space': 'pre-wrap',
    'width': '60%',
    'margin': 'auto',
    # 'table-layout': 'fixed',
})

calling_QC_html_table.set_style({
    'border-collapse': 'collapse',
    'word-break': 'normal',
    'white-space': 'pre-wrap',
    'width': '60%',
    'margin': 'auto',
})

# cells of table (<tbody><tr><td> or </td><th>)
raw_QC_html_table.set_data_cell_style({
    'font-family': 'arial',
    'font-size': '14px',
    'color': '#333333',
    'border-width': '1px',
    'border-color': '#A5A5A5',
    'border-style': 'solid',
    'padding': '8px',
})

align_QC_html_table.set_data_cell_style({
    'font-family': 'arial',
    'font-size': '14px',
    'color': '#333333',
    'border-width': '1px',
    'border-color': '#A5A5A5',
    'border-style': 'solid',
    'padding': '8px',
})
calling_QC_html_table.set_data_cell_style({
    'font-family': 'arial',
    'font-size': '14px',
    'color': '#333333',
    'border-width': '1px',
    'border-color': '#A5A5A5',
    'border-style': 'solid',
    'padding': '8px',
})

raw_QC_html_table.set_data_row_style({
    'align': 'center',
})
align_QC_html_table.set_data_row_style({
    'align': 'center',
})
calling_QC_html_table.set_data_row_style({
    'align': 'center',
})

# header of table
raw_QC_html_table.set_header_row_style({
    'color': '#fff',
    'background-color': '#48a6fb',
    'font-size': '15px',
})

align_QC_html_table.set_header_row_style({
    'color': '#fff',
    'background-color': '#48a6fb',
    'font-size': '16px',
})
calling_QC_html_table.set_header_row_style({
    'color': '#fff',
    'background-color': '#48a6fb',
    'font-size': '16px',
})
raw_QC_html_table.set_header_cell_style({
    'padding': '15px',
})
align_QC_html_table.set_header_cell_style({
    'padding': '15px',
})
calling_QC_html_table.set_header_cell_style({
    'padding': '15px',
    'border-width': '1px',
    'border-color': '#fff',
    'border-style': 'solid',
})

i = 0
for row in raw_QC_html_table.iter_data_rows():
    if i % 2 == 0:
        row.set_style({
            'background-color': '#fefdfa',
        })
    i = i + 1

j = 0
for row in align_QC_html_table.iter_data_rows():
    if j % 2 == 0:
        row.set_style({
            'background-color': '#fefdfa',
        })
    j = j + 1

q = 0
for row in calling_QC_html_table.iter_data_rows():
    if q % 2 == 0:
        row.set_style({
            'background-color': '#fefdfa',
        })
    q = q + 1

raw_QC_html_table[1][0].set_style({
    'background-color': '#F5F5F5',
    'width': '30%',
    'font-size': '16px',
    'color': '#3B3B3B',
    'font-weight': 'bold',
    'font-style': 'italic',
})

align_QC_html_table[1][0].set_style({
    'background-color': '#F5F5F5',
    'width': '30%',
    'font-size': '16px',
    'color': '#3B3B3B',
    'font-weight': 'bold',
    'font-style': 'italic',
})

calling_QC_html_table[2][0].set_style({
    'background-color': '#F5F5F5',
    'width': '30%',
    'font-size': '16px',
    'color': '#3B3B3B',
    'font-weight': 'bold',
    'font-style': 'italic',
})

align_QC_html_table[1][0].set_style({
    'background-color': '#F5F5F5',
})

calling_QC_html_table[1].set_cell_style({
    'background-color': '#48a6fb',
})

HEADER = '''
<!DOCTYPE html> 
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <title>DIVS Report</title>
        <script src="./releases/8.9.0/js/anychart-core.min.js"></script>
        <script src="./releases/8.9.0/js/anychart-venn.min.js"></script>
        <script src="./releases/8.9.0/themes/pastel.min.js"></script>
        <script src="./releases/8.9.0/js/anychart-base.min.js"></script>
        <script src="./releases/8.9.0/js/anychart-ui.min.js"></script>
        <script src="./releases/8.9.0/js/anychart-exports.min.js"></script>
        <script src="./releases/8.9.0/js/anychart-circular-gauge.min.js"></script>
        <script src="./releases/8.9.0/js/anychart-pie.min.js"></script>
        <script src="./releases/8.9.0/js/anychart-tag-cloud.min.js"></script>
        <script src="./releases/8.9.0/js/anychart-cartesian.min.js"></script>
        <script src="./releases/8.9.0/js/anychart-data-adapter.min.js"></script>
        <link href="./releases/8.9.0/css/anychart-ui.min.css" type="text/css" rel="stylesheet">
        <link href="./releases/8.9.0/anychart-font.min.css" type="text/css" rel="stylesheet">
        <link href="./releases/8.9.0/css2.css" type="text/css" rel="stylesheet">
        <style type="text/css">
          html,
          body {
            width: 100%;
            height: 100%;
            margin: 0;
            padding: 0;
            border : 'solid red 3px';
          }
          #figure1 {
            width: 70%;
            height: 70%;
            margin: 0% 15%;
            display: flex;
            #border:1px dashed #000; 
            align-items: center;
          }
          #figure2 {
            width: 70%;
            height: 70%;
            margin: 0% 15%;
            display: flex;
            #border:1px dashed #000;
            align-items: center;
          }
          #hexyvenn_SNV {
            width: 50%;
            height: 80%;
            padding: 0;
          }
          #hexygauge{
            width: 50%;
            height: 80%;
            padding: 0;
          }
          #hexypie {
            width: 50%;
            height: 80%;
            padding: 0;
          }
          #hexytagcloud {
            width: 50%;
            height: 80%;
            padding: 0;
          }
          #hexybar {
            width: 70%;
            height: 80%;
            margin: 0% 15%;
            padding: 0;
          }
          h1{
            font-size: 20px;
            margin: 3% 15%;
            color: #3399CC;
          }
          footer {
            margin: 0% 15%;
            background-color: #333333;
            padding: 1% 2%;
            #float: inline-block;
          }
          footer>p{
            color: #ffffff;
          }
          a:link{color: #6666FF;}
          a:visited{color:#990066;} 
          a:hover{color: #FF6666;}  
          a:active{color: #99CCCC;}
        </style>
        
        <script type="javascript">
            document.getElementById("demo").style.fontVariant = "small-caps";
        </script>
    </head>
    
    <body>
        <h1> DIVIS report of sample AC-WGS-1</h1>
    '''
CHALINES = '''
        <p> </p>
    '''
CONTAINER1_START = '''
        <div id="figure1">
'''
CONTAINER1_END = '''
        </div>
'''
CONTAINER2_START = '''
        <div id="figure2">
'''
CONTAINER2_END = '''
        </div>
'''
VENN_SNV = '''
        <div id="hexyvenn_SNV"></div>
        <script>
        anychart.onDocumentReady(function () {
            // set chart theme
            anychart.theme('pastel');
            var data = [
                {
                  x: 'A',
                  value: 100,
                  name: 'VarDict ',
                  tooltipTitle: 'v1.8.7',
                  normal: {fill: "#8ecafb 1"},
                  hovered: {fill: "#8ecafb 1"},
                  selected: {fill: "#8ecafb 1"}
                },
                {
                  x: 'B',
                  value: 100,
                  name: 'VarScan',
                  tooltipTitle: 'v2.4.9',
                  normal: {fill: "#ffeaa6 1"},
                  hovered: {fill: "#ffeaa6 1"},
                  selected: {fill: "#ffeaa6 1"}
                },
                {
                  x: 'C',
                  value: 100,
                  name: 'Strelka',
                  tooltipTitle: 'v1.2.1',
                  normal: {fill: "#ee957f 1"},
                  hovered: {fill: "#ee957f 1"},
                  selected: {fill: "#ee957f 1"}
                },
                {
                  x: 'D',
                  value: 100,
                  name: 'Pindel',
                  tooltipTitle: 'v1.11',
                  normal: {fill: "#66CC99 1"},
                  hovered: {fill: "#66CC99 1"},
                  selected: {fill: "#66CC99 1"}
                },
                {
                  x: ['A', 'B'],
                  value: 20,
                  name: '',
                  tooltipTitle: 'VarDict & VarScan',
                  tooltipDesc: 'Priority: VarScan',
                  normal: {fill: "#9fdebe 0.8"},
                  hovered: {fill: "#9fdebe 1"},
                  selected: {fill: "#9fdebe 1"},
                  hatchFill: {
                    type:"weave",
                    color: "#83c3a3"
                  }    
                },
                {
                  x: ['A', 'C'],
                  value: 20,
                  name: '',
                  tooltipTitle: 'VarDict & Strelka',
                  tooltipDesc: 'Priority: Strelka',
                  normal: {fill: "#a98caf 0.6"},
                  hovered: {fill: "#a98caf 1"},
                  selected: {fill: "#a98caf 1"},
                  hatchFill: {
                    type:"weave",
                    color: "#8b6b92"
                  }
                },
                {
                  x: ['A', 'D'],
                  value: 30,
                  name: '',
                  tooltipTitle: 'VarDict & Pindel',
                  tooltipDesc: 'Priority: Pindel',
                  normal: {fill: "#f5b57c 0.8"},
                  hovered: {fill: "#f5b57c 1"},
                  selected: {fill: "#f5b57c 1"},
                  hatchFill: {
                    type:"weave",
                    color: "#d09259"
                  }
                },
                {
                  x: ['B', 'C'],
                  value: 25,
                  name: '',
                  tooltipTitle: 'VarScan & Pindel',
                  tooltipDesc: 'Priority: VarScan',
                  normal: {fill: "#f5b57c 0.8"},
                  hovered: {fill: "#f5b57c 1"},
                  selected: {fill: "#f5b57c 1"},
                  hatchFill: {
                    type:"weave",
                    color: "#d09259"
                  }
                },
                {
                  x: ['B', 'D'],
                  value: 13,
                  name: '',
                  tooltipTitle: 'VarScan & Pindel',
                  tooltipDesc: 'Priority: VarScan',
                  normal: {fill: "#f5b57c 0.8"},
                  hovered: {fill: "#f5b57c 1"},
                  selected: {fill: "#f5b57c 1"},
                  hatchFill: {
                    type:"weave",
                    color: "#d09259"
                  }
                },
                 {
                  x: ['C', 'D'],
                  value: 13,
                  name: '',
                  tooltipTitle: 'Strelka & Pindel',
                  tooltipDesc: 'Priority: Strelka',
                  normal: {fill: "#f5b57c 0.8"},
                  hovered: {fill: "#f5b57c 1"},
                  selected: {fill: "#f5b57c 1"},
                  hatchFill: {
                    type:"weave",
                    color: "#d09259"
                  }
                },
                {
                  x: ['A', 'B', 'C'],
                  value: 30,
                  name: '',
                  tooltipTitle: 'VarDict & VarScan2 & Strelka',
                  tooltipDesc: 'Priority: VarScan2 > Strelka > VarDict',
                  label: {enabled:true, fontStyle: 'normal'},
                  normal: {fill: "#8392ab 0.9"},
                  hovered: {fill: "#8392ab 1"},
                  selected: {fill: "#8392ab 1"},
                  hatchFill: {
                    type:"percent40",
                    color: "#5f6b7d"
                  }
                },
                {
                  x: ['A', 'B', 'D'],
                  value: 18,
                  name: '',
                  tooltipTitle: 'VarDict & VarScan & Pindel',
                  tooltipDesc: 'Priority: VarScan2 > Pindel > VarDict',
                  label: {enabled:true, fontStyle: 'normal'},
                  normal: {fill: "#8392ab 0.9"},
                  hovered: {fill: "#8392ab 1"},
                  selected: {fill: "#8392ab 1"},
                  hatchFill: {
                    type:"percent40",
                    color: "#5f6b7d"
                  }
                },
                {
                  x: ['A', 'C', 'D'],
                  value: 18,
                  name: '',
                  tooltipTitle: 'VarDict & Strelka & Pindel',
                  tooltipDesc: 'Priority: VarScan2 > Pindel > Strelka',
                  label: {enabled:true, fontStyle: 'normal'},
                  normal: {fill: "#8392ab 0.9"},
                  hovered: {fill: "#8392ab 1"},
                  selected: {fill: "#8392ab 1"},
                  hatchFill: {
                    type:"percent40",
                    color: "#5f6b7d"
                  }
                },
                {
                  x: ['B', 'C', 'D'],
                  value: 10,
                  name: '',
                  tooltipTitle: 'VarScan2 & Strelka & Pindel',
                  tooltipDesc: 'Priority: VarScan2 > Pindel > Strelka',
                  label: {enabled:true, fontStyle: 'normal'},
                  normal: {fill: "#8392ab 0.9"},
                  hovered: {fill: "#8392ab 1"},
                  selected: {fill: "#8392ab 1"},
                  hatchFill: {
                    type:"percent40",
                    color: "#5f6b7d"
                  }
                }];
    
                // create venn diagram
                var chart = anychart.venn(data);
            
                // set chart title
                chart
                    .title()
                    .enabled(true)
                    .fontFamily('Roboto, sans-serif')
                    .fontSize(20)
                    .padding({ bottom: 30 })
                    .text('SNV Intersect in Callers');
            
                // set chart stroke
                chart.stroke('1 #fff');
            
                  // set labels settings
                chart
                    .labels()
                    .fontSize(12)
                    .fontColor('#5e6469')
                    .hAlign("center")
                    .vAlign("center")
                    .fontFamily('Roboto, sans-serif')
                    .fontWeight('500')
                    .format('{%Name}');
            
                // set intersections labels settings
                chart
                    .intersections()
                    .labels()
                    .fontStyle('italic')
                    .fontColor('#fff')
                    .format('{%Name}');
            
                // disable legend
                chart.legend(false);
            
                // set tooltip settings
                chart
                    .tooltip()
                    .titleFormat('{%tooltipTitle}')
                    .format("{%tooltipDesc}")
                    .background().fill("#000 0.5");
            
                // set container id for the chart
                chart.container('hexyvenn_SNV');
            
                // initiate chart drawing
                chart.draw();
                });
        </script>
    '''
GAUGE = '''
        <div id="hexygauge"></div>
            <script>
            var names = [
              'Missense_Mutation',
              'Nonsense_Mutation',
              'In_Frame_Ins',
              'START_CODON_SNP',
              'In_Frame_Del',
              'Frame_Shift_Del',
              'Splice_Site'
            ];
            var data = [23, 34, 67, 93, 56, 15, 75, 100];
            var dataSet = anychart.data.set(data);
            var palette = anychart.palettes
              .distinctColors()
              .items([
                '#64b5f6',
                '#1976d2', 
                '#ef6c00',
                '#ffd54f',
                '#455a64',
                '#96a6a6',
                '#dd2c00',
                '#00838f',
                '#00bfa5',
                '#ffa000',
              ]);
        
            var makeBarWithBar = function (gauge, radius, i, width) {
              var stroke = null;
              gauge
                .label(i)
                .text(names[i] + ', <span style="">' + data[i] + '%</span>') // color: #7c868e
                .useHtml(true);
              gauge
                .label(i)
                .hAlign('center')
                .vAlign('middle')
                .anchor('right-center')
                .padding(0, 10)
                .height(width / 2 + '%')
                .offsetY(radius + '%')
                .offsetX(0);
        
              gauge
                .bar(i)
                .dataIndex(i)
                .radius(radius)
                .width(width)
                .fill(palette.itemAt(i))
                .stroke(null)
                .zIndex(7);
              gauge
                .bar(i + 100)
                .dataIndex(7)
                .radius(radius)
                .width(width)
                .fill('#F5F4F4')
                .stroke(stroke)
                .zIndex(6);
        
              return gauge.bar(i);
            };
        
            anychart.onDocumentReady(function () {
              var gauge = anychart.gauges.circular();
              gauge.data(dataSet);
              gauge
                .fill('#fff')
                .stroke(null)
                .padding(0)
                .margin(100)
                .startAngle(0)
                .sweepAngle(270);
        
              var axis = gauge.axis().radius(100).width(1).fill(null);
              axis
                .scale()
                .minimum(0)
                .maximum(100)
                .ticks({ interval: 1 })
                .minorTicks({ interval: 1 });
              axis.labels().enabled(false);
              axis.ticks().enabled(false);
              axis.minorTicks().enabled(false);
              makeBarWithBar(gauge, 100, 0, 12);
              makeBarWithBar(gauge, 85, 1, 12);
              makeBarWithBar(gauge, 70, 2, 12);
              makeBarWithBar(gauge, 55, 3, 12);
              makeBarWithBar(gauge, 40, 4, 12);
              makeBarWithBar(gauge, 25, 5, 12);
              makeBarWithBar(gauge, 10, 6, 12);
        
              gauge.margin(0);
              gauge
                .title()
                .text('Variants Classification')
                .fontSize(20)
                .useHtml(true);
              gauge
                .title()
                .enabled(true)
                .hAlign('center')
                .padding(10)
                .margin([0, 0, 20, 0]);
        
              gauge.container('hexygauge');
              gauge.draw();
            }); 
             </script>          
'''
PIE = '''
        <div id="hexypie"></div>
        <script>
        anychart.onDocumentReady(function () {
            var chart = anychart.pie([
                {x: "SNP", value: 31989,
                   normal:  {fill: "#64b5f6"},              
                },
                {x: "DEL", value: 19609,
                   normal:  {fill: "#1976d2"},
                },
                {x: 'INS', value: 16429,
                  normal: {fill: "#ef6c00"},
                },
                {x: 'ONP', value: 2096,
                  normal: {fill: "#ffd54f"},
                },
                {x: 'DNP', value: 1763,
                  normal: {fill: "#6666CC"},
                },
                {x: 'TNP', value: 1325,
                  normal: {fill: "#455a64"},
                },
            ]);
            chart
                .title('Variant Type')
                .radius('43%')
                .innerRadius('30%');       
            var title = chart.title()
            title.fontSize(20)
            chart.normal().outline().enabled(true);
            chart.normal().outline().width("2%");
            chart.hovered().outline().width("4%");
            chart.selected().outline().width("3");
            chart.selected().outline().fill("#FF6666");
            chart.selected().outline().stroke(null);
            chart.selected().outline().offset(2);
            
            chart.container('hexypie');
            chart.draw();
        });
        </script>
'''
TAGCLOUD = '''
    <div id="hexytagcloud"> </div>
    <script>
    anychart.onDocumentReady(function () {
        // create data
        var data = %s

        // create a chart and set the data
        chart = anychart.tagCloud(data);
        chart
            .title('Top 100 mutated genes')
            
        var title = chart.title();
        title.fontSize(20);
        chart.container('hexytagcloud');
        chart.mode('spiral');
      
        chart.draw();
    });
    </script>
''' % tagcloud_data
BAR = '''
    <div id="hexybar"></div>
    <script>
        anychart.onDocumentReady(function () {
            var dataSet = anychart.data.set(%s);
            var firstSeriesData = dataSet.mapAs({ x: 0, value: 1 });
            var secondSeriesData = dataSet.mapAs({ x: 0, value: 2 });
            var chart = anychart.bar();
            chart.animation(true);
            chart.padding([10, 20, 5, 20]);
            chart.yScale().stackMode('value');
            chart
                .yAxis()
                .labels()
                .format(function () {
                  return Math.abs(this.value).toLocaleString();
                });
            chart.yAxis(0).title('Revenue in Dollars');
            chart.xAxis(0).overlapMode('allow-overlap');
        
            chart
                .xAxis(1)
                .enabled(true)
                .orientation('right')
                .overlapMode('allow-overlap');
        
            chart.title('Genetic Mutations by Chromosome');
            var title = chart.title()
            title.fontSize(20)
            chart.interactivity().hoverMode('by-x');
            chart
                .tooltip()
                .title(false)
                .separator(false)
                .displayMode('separated')
                .positionMode('point')
                .useHtml(true)
                .fontSize(12)
                .offsetX(5)
                .offsetY(0)
                .format(function () {
                    return (
                        '<span style="color: #D9D9D9"> </span>' +
                        Math.abs(this.value).toLocaleString()
                    );
                });
        
            var series;
        
            series = chart.bar(firstSeriesData);
            //series.name('Females').color('HotPink');#FF69B4 #FF99CC
            series.name('SNVs').color('#1976d2')
            series.tooltip().position('right').anchor('left-center');
            series = chart.bar(secondSeriesData);
            series.name('InDels').color('#FF1493');
            series.tooltip().position('left').anchor('right-center');
        
            chart
                .legend()
                .enabled(true)
                .inverted(true)
                .fontSize(13)
                .padding([0, 0, 20, 0]);
                
            chart.container('hexybar');
            chart.draw();
    });
</script>
''' % chr_bar_data
FOOTER = '''
    </body>
    <footer>
        <p> </p>
        <p> Posted by: DIVIS verison 1.0.3 at 2020/1/4 15:52 </p>
        <p> Contact information: <a href="mailto:hexy@sccas.cn"> hexy@sccas.cn </a> </p>
    </footer>
</html>
'''

table_1 = raw_QC_html_table.to_html()
table_2 = align_QC_html_table.to_html()
table_3 = calling_QC_html_table.to_html()

with open("hexy_test_v9.html", 'w', encoding='gb2312') as f:
    f.write(HEADER)
    f.write(html.unescape(table_1))
    f.write(CHALINES)
    f.write(html.unescape(table_2))
    f.write(CHALINES)
    f.write(html.unescape(table_3))
    f.write(CHALINES)
    f.write(CONTAINER1_START)
    f.write(VENN_SNV)
    f.write(GAUGE)
    f.write(CONTAINER1_END)
    f.write(CHALINES)
    f.write(CONTAINER2_START)
    f.write(PIE)
    f.write(CHALINES)
    f.write(TAGCLOUD)
    f.write(CONTAINER2_END)
    f.write(CHALINES)
    f.write(BAR)
    f.write(CHALINES)
    f.write(FOOTER)
