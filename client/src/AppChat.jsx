import { useState, useEffect } from "react";
import io from "socket.io-client";
import axios from "axios"; // Thư viện gọi API

const socket = io("http://localhost:3000");

function App() {
    const [message, setMessage] = useState("");
    const [messages, setMessages] = useState([]);

    // Lấy lịch sử tin nhắn khi load trang
    useEffect(() => {
        const fetchMessages = async () => {
            try {
                const response = await axios.get("http://localhost:3000/messages");
                setMessages(response.data);
            } catch (err) {
                console.error("Error fetching messages:", err);
            }
        };

        fetchMessages();

        // Lắng nghe tin nhắn mới từ server
        socket.on("receive_message", (newMessage) => {
            setMessages((prev) => [...prev, newMessage]);
        });
    }, []);

    // Gửi tin nhắn
    const sendMessage = () => {
        if (message.trim() !== "") {
            const newMessage = { sender: "User1", content: message }; // Gửi tin từ User1
            socket.emit("send_message", newMessage); // Gửi tin nhắn lên server
            setMessage(""); // Xóa nội dung input sau khi gửi
        }
    };

    return (
        <div>
            <h1>Chat Realtime</h1>
            <div>
                {messages.map((msg, index) => (
                    <p key={index}>
                        <strong>{msg.sender}:</strong> {msg.content}
                    </p>
                ))}
            </div>
            <input
                type="text"
                value={message}
                onChange={(e) => setMessage(e.target.value)}
            />
            <button onClick={sendMessage}>Send</button>
        </div>
    );
}

export default App;
