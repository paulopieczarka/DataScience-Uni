const Papa = require('papaparse')
const fs = require('fs')
const moment = require('moment')

// csv file.
let file = '../base/austin_crime01.csv'
let crimesContent = fs.readFileSync(file, "utf8")

// Read csv.
let csvFormat = {
    delimiter: ',',
    header: true,
    encoding: 'utf8'
}

let data = Papa.parse (crimesContent, { ...csvFormat, complete: onFileReaded})

function onFileReaded (results) {
    
    let { data } = results
    let districtKeys = ['A', 'AP', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'UK']
    let districts = []

    districtKeys.forEach (i => {
        districts[i] = data.filter(x => x.district === i)
    })

    for (let key in districts) {        
        districts[key] = fillEmptyRows(
            'latitude', 
            districts[key], 
            average(districts[key], 'latitude')
        )
            
        districts[key] = fillEmptyRows(
            'longitude', 
            districts[key],
            average(districts[key], 'longitude')
        )

        addFinishTime(districts[key], 'timestamp', 'clearance_date')
    }

    let resultData = []
    for (let key in districts) {
        resultData = resultData.concat(districts[key])
    }

    let valueToIndexResult = [
        stringValueToIndex(resultData, 'district'),
        stringValueToIndex(resultData, 'council_district_code'),
        stringValueToIndex(resultData, 'clearance_status'),
        stringValueToIndex(resultData, 'description'),
    ]

    let valueDescripions = valueToIndexResult.map(({key, description}) => (
        `${key},${description.join(',')}`
    ))
    
    // console.log(valueDescripions)

    console.log(resultData[0])    
    console.log(resultData[resultData.length-1])

    saveNewDatabase ('../base/result', resultData, valueDescripions)
}

function stringValueToIndex (resultSet, key, step=6) {
    let values = []
    resultSet.forEach(x => {
        if(!values.includes(x[key])) {
            values.push(x[key])
        }
    })

    let newResultSet = resultSet.map(x => {
        x[key] = values.indexOf(x[key])*step
        return x
    })

    return {
        key: key,
        description: values,
        array: newResultSet
    }
}

function fillEmptyRows (key, group, value) {
    return group.map(x => {
        if (x[key] === '') x[key] = value
        return x
    })
}

function saveNewDatabase (file, data, valuesDescription) {
    let csv = Papa.unparse(data, {
        ...csvFormat
    })
    
    fs.writeFileSync(`${file}.csv`, csv)
    console.log('Results saved.')    
    fs.writeFileSync(`${file}-descriptions.csv`, valuesDescription.join('\n'))
    console.log('Results description saved.')
}

function average (group, key) {
    let sum = 0
    let list = group.filter(x => x[key] !== '')
    list.forEach(v => sum += parseFloat(v[key]))
    return sum / list.length
}

function addFinishTime (group, start, end) {
    group.forEach(x => {
        if(x[start] !== '' && x[end] !== ''){
            let startTime = moment(x[start])
            let endTime = moment(x[end])
            x['clearance_days'] = endTime.diff(startTime, 'days', true)
        }
    })

    let maxDays = group.filter(x => x['clearance_days']).sort((a, b) => b['clearance_days'] - a['clearance_days'])[0]
    group.forEach(x => {
        if (!x['clearance_days']) {
            x['clearance_days'] = maxDays['clearance_days']
        }
    })
}
