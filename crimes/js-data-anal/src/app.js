const Papa = require('papaparse')
const fs = require('fs')

// csv file.
let file = '../base/austin_crime.csv'
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
        console.log(
            `-> ${key} = (`, 
            average(districts[key], 'latitude'),
            ',',
            average(districts[key], 'longitude'),
            ')')
        
            districts[key] = fillEmptyRows('latitude', districts[key], average(districts[key], 'latitude'))
            districts[key] = fillEmptyRows('longitude', districts[key], average(districts[key], 'longitude'))
    }

    let resultData = []
    for (let key in districts) {
        resultData = resultData.concat(districts[key])
    }

    saveNewDatabase ('../base/result.csv', resultData)
}

function fillEmptyRows (key, group, value) {
    return group.map(x => {
        if (x[key] === '') x[key] = value
        return x
    })
}

function saveNewDatabase (file, data) {
    let csv = Papa.unparse(data, {
        ...csvFormat
    })
    
    fs.writeFileSync(file, csv)
    console.log('Results saved.')
}

function average (group, key) {
    let sum = 0
    let list = group.filter(x => x[key] !== '')
    list.forEach(v => sum += parseFloat(v[key]))
    return sum / list.length
}
