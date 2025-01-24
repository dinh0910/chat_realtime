const mongoose = require("mongoose");

const MessageSchema = new mongoose.Schema({
    sender: { type: String, required: true }, // Người gửi
    content: { type: String, required: true }, // Nội dung tin nhắn
    timestamp: { type: Date, default: Date.now }, // Thời gian gửi
});

module.exports = mongoose.model("Message", MessageSchema);
