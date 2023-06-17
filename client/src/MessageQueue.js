import * as amqp from 'amqplib';

class MessageQueue {
    constructor() {
        this.queueName = 'button_sequence';
        this.connection = null;
        this.channel = null;
    }

    async connect() {
        if (!this.connection) {
            this.connection = await amqp.connect('amqp://localhost');
            this.channel = await this.connection.createChannel();
            await this.channel.assertQueue(this.queueName);
        }
    }

    async sendMessage(sequence) {
        await this.connect();
        this.channel.sendToQueue(this.queueName, Buffer.from(JSON.stringify(sequence)));
    }
}

export default MessageQueue;
