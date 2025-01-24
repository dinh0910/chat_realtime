const express = require("express");
const http = require("http");
const { Server } = require("socket.io");
const cors = require("cors");
const mongoose = require("mongoose");
const Message = require("./models/Message");

const app = express();
const server = http.createServer(app);
const io = new Server(server, {
    cors: {
        origin: "http://localhost:5173", // Cho phép truy cập từ frontend
        methods: ["GET", "POST"],
    },
});

// Kết nối MongoDB
mongoose
    .connect("mongodb://localhost:27017/chat_realtime", {
        useNewUrlParser: true,
        useUnifiedTopology: true,
    })
    .then(() => console.log("Connected to MongoDB"))
    .catch((err) => console.error("MongoDB connection error:", err));

// Cấu hình CORS cho Express
app.use(cors({
    origin: "http://localhost:5173",
    methods: ["GET", "POST"],
    credentials: true,
}));

// Xử lý sự kiện Socket.IO
io.on("connection", (socket) => {
    console.log("User connected:", socket.id);

    socket.on("send_message", async (data) => {
        try {
            const newMessage = new Message({
                sender: data.sender,
                content: data.content,
            });
            const savedMessage = await newMessage.save();
            io.emit("receive_message", savedMessage);
        } catch (err) {
            console.error("Error saving message:", err);
        }
    });

    socket.on("disconnect", () => {
        console.log("User disconnected:", socket.id);
    });
});

// API lấy lịch sử tin nhắn
app.get("/messages", async (req, res) => {
    try {
        const messages = await Message.find().sort({ createdAt: 1 });
        res.json(messages);
    } catch (err) {
        res.status(500).json({ error: "Failed to fetch messages" });
    }
});

// Khởi động server
server.listen(3000, () => {
    console.log("Server is running on http://localhost:3000");
});
