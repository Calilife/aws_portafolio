import React from 'react';
import ReactDOM from 'react-dom';
import ExampleWork from './example-work'

const myWork = [
    {
        'title': "Wordpress Work", 
        'image': {
            'desc': "This is an example of the work I have done using Wordpress",
            'src': "images/example1.png",
            'comment': ""
        }
    }, 
    {
        'title': "Adobe DX Design", 
        'image': {
            'desc': "Designs I completed for personal use and development",
            'src': "images/example2.png",
            'comment': ""
        }
    },
    {
        'title': "AWS Serverless", 
        'image': {
            'desc': "Live example of a serverless deployment that cost $1 dollar a month",
            'src': "images/aws_architecture.PNG",
            'comment': ""
        }
    }
]

ReactDOM.render(<ExampleWork work={myWork} />, document.getElementById('example-work'))

