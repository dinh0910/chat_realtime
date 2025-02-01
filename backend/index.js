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
        origin: "http://localhost:5173",
        methods: ["GET", "POST"],
    },
});

app.use(cors());

// Kết nối MongoDB
mongoose
    .connect("mongodb://localhost:27017/chat_realtime", {
        useNewUrlParser: true,
        useUnifiedTopology: true,
    })
    .then(() => console.log("Connected to MongoDB"))
    .catch((err) => console.error("MongoDB connection error:", err));

// Danh sách user online
const onlineUsers = new Map(); // Key: socket.id, Value: username

// Xử lý sự kiện Socket.IO
io.on("connection", (socket) => {
    console.log("User connected:", socket.id);

    // Nhận thông tin user khi kết nối
    socket.on("user_connected", (username) => {
        onlineUsers.set(socket.id, username); // Lưu user vào danh sách online
        console.log(`${username} joined the chat`);
        io.emit("update_user_list", Array.from(onlineUsers.values())); // Gửi danh sách user online tới tất cả
    });

    // Khi người dùng gửi tin nhắn
    socket.on("send_message", async (data) => {
        try {
            const { sender, content } = data;

            // Lưu tin nhắn vào MongoDB
            const newMessage = new Message({
                sender,
                content,
            });
            const savedMessage = await newMessage.save();

            // Gửi tin nhắn đến tất cả các user
            io.emit("receive_message", savedMessage);
        } catch (err) {
            console.error("Error saving message:", err);
        }
    });

    // Khi người dùng ngắt kết nối
    socket.on("disconnect", () => {
        const username = onlineUsers.get(socket.id);
        if (username) {
            onlineUsers.delete(socket.id); // Xóa user khỏi danh sách online
            console.log(`${username} left the chat`);
            io.emit("update_user_list", Array.from(onlineUsers.values())); // Gửi danh sách user cập nhật
        }
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
