# 配置.env文件
本项目需要您的模型API是否兼容OpenAI API的格式，您可以查看下方表格，确认您的模型供应商（或者模型推理框架服务）是否支持。
> 注：本项目需要您的模型支持function call的功能（在未来，我们将适配不支持function call的模型，以供兼容更多的模型）

以下是截至2025年5月主流模型供应商及推理引擎的完整汇总表格，包含名称、API地址、文档地址及OpenAI API兼容性标记：

### **一、模型供应商（兼容OpenAI API格式）**
| 供应商名称       | API地址                                      | API文档地址                                   | 支持OpenAI格式 |
|------------------|---------------------------------------------|---------------------------------------------|----------------|
| **智谱清言**     | `https://open.bigmodel.cn/api/paas/v4`      | [文档](https://bigmodel.cn/dev/api/thirdparty-frame/openai-sdk) | ✅             |
| **科大讯飞星火**  | `https://spark-api-open.xf-yun.com/v1`      | [文档](https://www.xfyun.cn/doc/spark/HTTP调用文档.html#_7-使用openai-sdk请求示例) | ✅             |
| **百川大模型**    | `https://api.baichuan-ai.com/v1`            | [文档](https://platform.baichuan-ai.com/docs/api#python-client) | ✅             |
| **豆包大模型**    | `https://ark.cn-beijing.volces.com/api/v3`  | [文档](https://www.volcengine.com/docs/82379/1330626) | ✅             |
| **月之暗面**      | `https://api.moonshot.cn/v1`                | [文档](https://platform.moonshot.cn/docs/guide/migrating-from-openai-to-kimi#关于-api-兼容性) | ✅             |
| **通义千问**      | `https://dashscope.aliyuncs.com/compatible-mode/v1` | [文档](https://help.aliyun.com/zh/model-studio/getting-started/first-api-call-to-qwen) | ✅             |
| **腾讯混元**      | `https://api.hunyuan.cloud.tencent.com/v1`  | [文档](https://cloud.tencent.com/document/product/1729/111007) | ✅             |
| **商汤日日新**    | `https://api.sensenova.cn/compatible-mode/v1` | [文档](https://www.sensecore.cn/help/docs/model-as-a-service/nova/overview/compatible-mode) | ✅             |
| **DeepSeek**     | `https://api.deepseek.com/v1`               | [文档](https://platform.deepseek.com/api-docs) | ✅             |
| **硅基流动**     | `https://api.siliconflow.cn/v1`             | [文档](https://cloud.siliconflow.cn/docs)   | ✅             |
| **360智脑**      | 需企业申请（未公开统一API）                 | [测评报告](https://www.cluebenchmarks.com)  | ❌             |
| **OpenAI**       | `https://api.openai.com/v1`                | [官方文档](https://platform.openai.com/docs) | ✅             |
| **Anthropic**    | `https://api.anthropic.com/v1`             | [文档](https://docs.anthropic.com)           | ⚠️（部分兼容） |

### **二、开源推理引擎（兼容OpenAI API）**
| 引擎名称       | API地址（本地部署）       | 文档地址                                   | 支持OpenAI格式 |
|----------------|--------------------------|-------------------------------------------|----------------|
| **vLLM**       | `http://localhost:8000/v1` | [GitHub](https://github.com/vllm-project/vllm) | ✅             |
| **SGLang**     | `http://localhost:3000/v1` | [GitHub](https://github.com/sgl-project/sglang) | ✅             |
| **Ollama**     | `http://localhost:11434/v1` | [官网](https://ollama.ai)                  | ✅             |
| **LMDeploy**   | `http://localhost:23333/v1` | [文档](https://lmdeploy.readthedocs.io)    | ✅             |
| **TensorRT-LLM** | `http://localhost:8000/v1` | [NVIDIA文档](https://github.com/NVIDIA/TensorRT-LLM) | ✅             |
| **Mooncake**   | 需定制部署               | [GitHub](https://github.com/mooncake-project) | ❌             |

### **关键说明**
1. **兼容性标记**：  
   - ✅：完全兼容OpenAI API格式。  
   - ⚠️：需调整部分参数或接口。  
   - ❌：不兼容或需深度适配。  
2. **国内服务**：如360智脑、百度等可能需企业认证或创建应用。  
3. **自托管引擎**：vLLM、Ollama等需自行部署，硬件要求较高。


### **配置文件注意事项**
- OPENAI_BASE_URL：请填写您所使用的模型供应商的API地址。
  - 这里的URL并非完整的API地址，而是base_url, 其完整路径为： `https://<base_url>/chat/completions` 
  - 假设您的API地址为：`https://api.deepseek.com/v1/chat/completions`， 则填写`https://api.deepseek.com/v1` 即可
  - 因此，判断模型API是否兼容OpenAI API格式，可以简单的判断API地址的格式是否是  `http://xxx/v1/chat/completions` 
  - 也有的模型供应商的API地址并不包含`v1` 等版本号，此时您可以尝试将`v1` 等版本号去掉，比如硅基流动，直接填写`https://api.siliconflow.cn` 即可。
- OPENAI_API_KEY：请填写您的OpenAI API Key。
  - **如果您是使用（vLLM、Ollama等）私有化部署的模型**，您可能没有手动设置API Key，此时这里您可以**直接填`sk-api-key`**。
  - 私有化部署可能没有API Key，但您此处不得为空，所以随意填写一个字符串，确保不为空即可。
- OPENAI_MODEL：请填写您所使用的模型的ID。


# Configuring the .env File  
This project requires your model API to be compatible with the OpenAI interface format. Please refer to the table below to confirm whether your model provider (model inference framework service) supports it.  
> Note: This project requires your model to support function call capabilities (in the future, we will adapt to models that do not support function calls to ensure compatibility with more models).  

Below is a comprehensive table of mainstream model providers and inference engines as of May 2025, including names, API addresses, documentation links, and OpenAI API compatibility markers:  

### **I. Model Providers (Compatible with OpenAI API Format)**  
| Provider Name       | API Address                                      | Documentation Link                                   | OpenAI Format Support |
|---------------------|-------------------------------------------------|-----------------------------------------------------|-----------------------|
| **Zhipu Qingyan**   | `https://open.bigmodel.cn/api/paas/v4`         | [Docs](https://bigmodel.cn/dev/api/thirdparty-frame/openai-sdk) | ✅                    |
| **iFlytek Spark**   | `https://spark-api-open.xf-yun.com/v1`         | [Docs](https://www.xfyun.cn/doc/spark/HTTP调用文档.html#_7-使用openai-sdk请求示例) | ✅                    |
| **Baichuan**       | `https://api.baichuan-ai.com/v1`               | [Docs](https://platform.baichuan-ai.com/docs/api#python-client) | ✅                    |
| **Doubao**         | `https://ark.cn-beijing.volces.com/api/v3`     | [Docs](https://www.volcengine.com/docs/82379/1330626) | ✅                    |
| **Moonshot AI**    | `https://api.moonshot.cn/v1`                   | [Docs](https://platform.moonshot.cn/docs/guide/migrating-from-openai-to-kimi#关于-api-兼容性) | ✅                    |
| **Tongyi Qianwen** | `https://dashscope.aliyuncs.com/compatible-mode/v1` | [Docs](https://help.aliyun.com/zh/model-studio/getting-started/first-api-call-to-qwen) | ✅                    |
| **Tencent Hunyuan** | `https://api.hunyuan.cloud.tencent.com/v1`     | [Docs](https://cloud.tencent.com/document/product/1729/111007) | ✅                    |
| **SenseTime Nova** | `https://api.sensenova.cn/compatible-mode/v1`  | [Docs](https://www.sensecore.cn/help/docs/model-as-a-service/nova/overview/compatible-mode) | ✅                    |
| **DeepSeek**       | `https://api.deepseek.com/v1`                  | [Docs](https://platform.deepseek.com/api-docs)       | ✅                    |
| **SiliconFlow**    | `https://api.siliconflow.cn/v1`                | [Docs](https://cloud.siliconflow.cn/docs)           | ✅                    |
| **360 AI Brain**  | Enterprise application required (no public API) | [Evaluation Report](https://www.cluebenchmarks.com) | ❌                    |
| **OpenAI**        | `https://api.openai.com/v1`                   | [Official Docs](https://platform.openai.com/docs)   | ✅                    |
| **Anthropic**     | `https://api.anthropic.com/v1`                | [Docs](https://docs.anthropic.com)                  | ⚠️ (Partial compatibility) |

### **II. Open-Source Inference Engines (Compatible with OpenAI API)**  
| Engine Name     | Local API Address         | Documentation Link                           | OpenAI Format Support |
|-----------------|---------------------------|---------------------------------------------|-----------------------|
| **vLLM**        | `http://localhost:8000/v1` | [GitHub](https://github.com/vllm-project/vllm) | ✅                    |
| **SGLang**      | `http://localhost:3000/v1` | [GitHub](https://github.com/sgl-project/sglang) | ✅                    |
| **Ollama**      | `http://localhost:11434/v1` | [Website](https://ollama.ai)                | ✅                    |
| **LMDeploy**    | `http://localhost:23333/v1` | [Docs](https://lmdeploy.readthedocs.io)     | ✅                    |
| **TensorRT-LLM** | `http://localhost:8000/v1` | [NVIDIA Docs](https://github.com/NVIDIA/TensorRT-LLM) | ✅                    |
| **Mooncake**    | Custom deployment required | [GitHub](https://github.com/mooncake-project) | ❌                    |

### **Key Notes**  
1. **Compatibility Markers**:  
   - ✅: Fully compatible with OpenAI API format.  
   - ⚠️: Requires partial parameter or interface adjustments.  
   - ❌: Not compatible or requires deep adaptation.  
2. **Domestic Services**: Providers like 360 AI Brain or Baidu may require enterprise authentication or application creation.  
3. **Self-Hosted Engines**: vLLM, Ollama, etc., require self-deployment and have high hardware requirements.  

### **Configuration File Notes**  
- **OPENAI_BASE_URL**: Enter the API address of your chosen model provider.  
  - This URL is not the full API address but the base URL. The full path is: `https://<base_url>/chat/completions`.  
  - For example, if your API address is `https://api.deepseek.com/v1/chat/completions`, simply enter `https://api.deepseek.com/v1`.  
- **OPENAI_API_KEY**: Enter your OpenAI API key.  
  - **If you are using a privately deployed model (e.g., vLLM, Ollama)**, you may not have manually set an API key. In this case, you can **enter `sk-api-key` directly**.  
  - Privately deployed models may not require an API key, but this field cannot be empty. You can enter any string to ensure it is not blank.  
- **OPENAI_MODEL**: Enter the ID of the model you are using.
