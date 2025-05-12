// 引入工具函数
// 使用getBasePath()获取API基础路径
const BASE_PATH = getBasePath();

// 定义API请求函数
async function submitQuestion() {
    const question = document.getElementById('question').value;
    const agentUrl = document.getElementById('agentUrl').value || 'https://agent-search.ai/ad.json';
    
    if (!question) {
        alert('请输入问题');
        return;
    }

    // 显示加载状态
    document.getElementById('submitBtn').disabled = true;
    document.getElementById('submitBtn').textContent = '处理中...';
    
    // 清空之前的结果
    document.getElementById('result').innerHTML = '';
    document.getElementById('visitedUrls').innerHTML = '';
    
    try {
        const response = await fetch(`${BASE_PATH}/api/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                question: question,
                agent_url: agentUrl
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // 显示结果
        document.getElementById('result').innerHTML = data.content;
        
        // 显示访问过的URL
        if (data.visited_urls && data.visited_urls.length > 0) {
            const urlsList = document.createElement('ul');
            data.visited_urls.forEach(url => {
                const li = document.createElement('li');
                li.textContent = url;
                li.style.wordBreak = 'break-word'; // 确保长URL能够换行显示
                urlsList.appendChild(li);
            });
            document.getElementById('visitedUrls').appendChild(urlsList);
        }
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('result').innerHTML = `错误: ${error.message}`;
    } finally {
        // 恢复按钮状态
        document.getElementById('submitBtn').disabled = false;
        document.getElementById('submitBtn').textContent = '提交问题';
    }
} 