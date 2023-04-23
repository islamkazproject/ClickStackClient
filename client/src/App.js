import React, {useState, useEffect} from 'react';
import axios from 'axios';
import MessageQueue from './MessageQueue';

function App() {

    const [sequence, setSequence] = useState([]);

    const handleClick = (buttonNumber) => {
        // Добавляем номер кнопки в последовательность
        setSequence((prevSequence) => [...prevSequence, buttonNumber]);
    };
/*    const handleClick1 = async () => {
        try {
            const response = await axios.post('http://localhost:3000/button1', {button: '1'});
            console.log(response.data);
        } catch (error) {
            console.error(error);
        }
    }

    const handleClick2 = async () => {
        try {
            const response = await axios.post('http://localhost:3000/button2', {button: '2'});
            console.log(response.data);
        } catch (error) {
            console.error(error);
        }
    }

    const handleClick3 = async () => {
        try {
            const response = await axios.post('http://localhost:3000/button3', {button: '3'});
            console.log(response.data);
        } catch (error) {
            console.error(error);
        }
    }

 */
    useEffect(() => {
        // Создаем экземпляр MessageQueue для обмена сообщениями между клиентом и сервером
        const messageQueue = new MessageQueue();

        // Отправляем последовательность на серверную часть, когда она изменяется
        if (sequence.length === 3) {
            axios.post('http://localhost:3000/api/sequence', { sequence })
                .then((response) => {
                    // Принимаем последовательность, возвращенную серверной частью
                    const receivedSequence = response.data.sequence;
                    console.log(receivedSequence);

                    // Отправляем последовательность на сервер RabbitMQ
                    messageQueue.sendMessage(receivedSequence);
                })
                .catch((error) => {
                    console.log(error);
                });
        }
    }, [sequence]);

    return (
        <div className="App">
            <button onClick={() => handleClick(1)}>Button 1</button>
            <button onClick={() => handleClick(2)}>Button 2</button>
            <button onClick={() => handleClick(3)}>Button 3</button>
        </div>
    );
}

export default App;
