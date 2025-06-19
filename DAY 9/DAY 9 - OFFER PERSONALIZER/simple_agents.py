import os
import json
import requests
from dataclasses import dataclass
from typing import Dict, List
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.docstore.document import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from bs4 import BeautifulSoup
import time
import re

@dataclass
class CandidateProfile:
    name: str = ""
    experience: float = 0.0
    role: str = ""
    company: str = ""
    location: str = ""
    skills: List[str] = None
    education: List[str] = None

class RAGRetriever:
    """Enhanced RAG implementation with FAISS"""
    
    def __init__(self, api_key: str):
        self.embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=api_key)
        self.llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=api_key, temperature=0.1)
        self.vectorstore = None
        self._build_knowledge_base()
    
    def _build_knowledge_base(self):
        """Build comprehensive knowledge base"""
        documents = self._create_market_documents()
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=512,
            chunk_overlap=50,
            separators=["\n\n", "\n", ". ", " "]
        )
        
        splits = text_splitter.split_documents(documents)
        self.vectorstore = FAISS.from_documents(splits, self.embeddings)
    
    def _create_market_documents(self) -> List[Document]:
        """Create comprehensive market knowledge documents"""
        return [
            Document(page_content="""
            Google Software Engineer L3 Bangalore: Base ₹18L, Total ₹23L, Stock ₹3L, Bonus ₹2L
            Experience: 0-2 years, Tier1 company, Growth rate: 15% YoY
            Skills premium: System Design +20%, ML +25%, Cloud +15%
            """, metadata={"company": "Google", "level": "L3"}),
            
            Document(page_content="""
            Microsoft Software Engineer II Bangalore: Base ₹30L, Total ₹42L, Stock ₹7L, Bonus ₹5L
            Experience: 2-5 years, Tier1 company, RSU vesting: 25% annually
            Market position: 75th percentile, Skills: Azure +18%, .NET +12%
            """, metadata={"company": "Microsoft", "level": "SDE2"}),
            
            Document(page_content="""
            Amazon SDE2 Bangalore: Base ₹28L, Total ₹40L, Stock ₹7L, Bonus ₹5L
            Experience: 2-5 years, Signing bonus: ₹3L, Performance bonus: 10-20%
            AWS skills premium: 20%, System design critical
            """, metadata={"company": "Amazon", "level": "SDE2"}),
            
            Document(page_content="""
            Startup trends 2024: Base growth 12%, equity 30-50% of package
            Remote premium: 5-10%, AI/ML roles: 25% above average
            Location: Mumbai +10%, Delhi +5%, Pune -12%, Chennai -15%
            """, metadata={"type": "trends", "year": "2024"})
        ]
    
    def retrieve(self, query: str, k: int = 3) -> List[Document]:
        """Retrieve relevant documents"""
        return self.vectorstore.similarity_search(query, k=k)

class MarketBenchmarkRetrieverAgent:
    """Agent 1: Market data retrieval with RAG"""
    
    def __init__(self, api_key: str, rag_retriever: RAGRetriever):
        self.rag = rag_retriever
        self.llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=api_key, temperature=0.1)
        
    def _scrape_live_data(self, query: str) -> str:
        """Simplified live data scraping"""
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            # Simplified mock data for demo
            mock_data = {
                "software engineer": "Market range: ₹15-35L, Average: ₹25L",
                "senior software engineer": "Market range: ₹35-60L, Average: ₹47L",
                "staff engineer": "Market range: ₹60-100L, Average: ₹80L"
            }
            return mock_data.get(query.lower(), f"Market data for {query}: Competitive packages")
        except:
            return f"Live data unavailable for {query}"
    
    def _search_knowledge_base(self, query: str) -> str:
        """RAG-powered knowledge search"""
        docs = self.rag.retrieve(query, k=3)
        context = "\n".join([doc.page_content for doc in docs])
        
        prompt = ChatPromptTemplate.from_template("""
        Based on market knowledge, provide salary insights for: {query}
        
        Context: {context}
        
        Provide specific figures and trends.
        """)
        
        chain = prompt | self.llm | StrOutputParser()
        return chain.invoke({"context": context, "query": query})
    
    def retrieve_market_data(self, role: str, location: str, company_type: str) -> Dict:
        """Main retrieval method"""
        query = f"{role} {location} {company_type} compensation"
        
        rag_results = self._search_knowledge_base(query)
        live_data = self._scrape_live_data(role)
        
        return {
            "rag_insights": rag_results,
            "live_data": live_data,
            "query": query,
            "timestamp": time.time()
        }

class CandidatePositioningAgent:
    """Agent 2: Enhanced candidate positioning"""
    
    def __init__(self, api_key: str, rag_retriever: RAGRetriever):
        self.llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=api_key, temperature=0.2)
        self.rag = rag_retriever
    
    def analyze_with_transformers(self, profile: CandidateProfile) -> Dict:
        """Enhanced analysis simulating transformer capabilities"""
        # Simulate NER extraction
        text = f"{profile.name} {profile.experience} years {profile.role} {profile.company} {' '.join(profile.skills or [])}"
        
        # Extract entities using regex patterns (simulating NER)
        entities = []
        
        # Extract companies
        companies = re.findall(r'\b(?:Google|Microsoft|Amazon|Meta|Apple|Netflix|Uber|LinkedIn|Flipkart|Paytm|TCS|Infosys)\b', text, re.IGNORECASE)
        entities.extend(companies)
        
        # Extract technologies
        technologies = re.findall(r'\b(?:Python|Java|JavaScript|React|Node|AWS|Kubernetes|Machine Learning|Docker|MongoDB)\b', text, re.IGNORECASE)
        entities.extend(technologies)
        
        # Enhanced analysis
        experience_tier = self._classify_experience(profile.experience)
        company_tier = self._assess_company_tier(profile.company)
        skills_premium = self._calculate_skills_premium(profile.skills or [])
        market_segment = self._determine_market_segment(experience_tier, company_tier, skills_premium)
        
        return {
            "experience_tier": experience_tier,
            "company_tier": company_tier,
            "skills_premium": skills_premium,
            "extracted_entities": list(set(entities)),
            "market_segment": market_segment,
            "positioning_score": self._calculate_positioning_score(profile),
            "competitive_advantages": self._identify_advantages(profile)
        }
    
    def _classify_experience(self, years: float) -> str:
        """Enhanced experience classification"""
        if years < 1: return "Entry Level (0-1 years) - Junior segment"
        elif years < 3: return "Junior (1-3 years) - Growth segment"
        elif years < 6: return "Mid-level (3-6 years) - Competitive segment"
        elif years < 10: return "Senior (6-10 years) - Premium segment"
        else: return "Staff+ (10+ years) - Executive segment"
    
    def _assess_company_tier(self, company: str) -> str:
        """Enhanced company tier assessment"""
        if not company:
            return "Unknown - Standard positioning"
            
        company_lower = company.lower()
        
        tier1_keywords = ['google', 'microsoft', 'amazon', 'meta', 'apple', 'netflix', 'uber', 'linkedin']
        tier2_keywords = ['flipkart', 'paytm', 'ola', 'swiggy', 'zomato', 'razorpay', 'cred', 'phonepe']
        unicorn_keywords = ['byju', 'unacademy', 'vedantu', 'meesho', 'sharechat']
        service_keywords = ['tcs', 'infosys', 'wipro', 'cognizant', 'accenture', 'capgemini', 'hcl']
        
        if any(keyword in company_lower for keyword in tier1_keywords):
            return "Tier1 (FAANG) - Premium positioning with 40-60% market premium"
        elif any(keyword in company_lower for keyword in tier2_keywords):
            return "Tier2 (Established Unicorn) - Strong positioning with 20-30% premium"
        elif any(keyword in company_lower for keyword in unicorn_keywords):
            return "Tier2 (Growing Unicorn) - Good positioning with 15-25% premium"
        elif any(keyword in company_lower for keyword in service_keywords):
            return "Service Company - Standard positioning with market-rate compensation"
        else:
            return "Startup/Other - Moderate positioning with equity upside potential"
    
    def _calculate_skills_premium(self, skills: List[str]) -> Dict:
        """Enhanced skills premium calculation"""
        premium_skills = {
            'machine learning': 25, 'artificial intelligence': 25, 'deep learning': 22,
            'system design': 20, 'microservices': 18, 'kubernetes': 15,
            'aws': 15, 'azure': 12, 'gcp': 12, 'google cloud': 12,
            'react': 10, 'angular': 8, 'vue': 8, 'node.js': 10,
            'python': 8, 'golang': 12, 'rust': 15, 'scala': 12,
            'docker': 10, 'jenkins': 8, 'terraform': 12,
            'mongodb': 8, 'postgresql': 6, 'redis': 8,
            'kafka': 12, 'elasticsearch': 10, 'spark': 15
        }
        
        matched_skills = []
        total_premium = 0
        
        for skill in skills:
            skill_lower = skill.lower()
            for premium_skill, premium in premium_skills.items():
                if premium_skill in skill_lower:
                    matched_skills.append({"skill": skill, "premium": premium})
                    total_premium += premium
        
        return {
            "total_premium": min(total_premium, 50),  # Cap at 50%
            "matched_skills": matched_skills,
            "skill_count": len(matched_skills),
            "premium_tier": "High" if total_premium > 40 else "Medium" if total_premium > 20 else "Standard"
        }
    
    def _determine_market_segment(self, experience: str, company: str, skills_premium: Dict) -> str:
        """Determine overall market segment"""
        premium_score = 0
        
        if "Staff+" in experience or "Senior" in experience:
            premium_score += 3
        elif "Mid-level" in experience:
            premium_score += 2
        elif "Junior" in experience:
            premium_score += 1
        
        if "Tier1" in company:
            premium_score += 3
        elif "Tier2" in company:
            premium_score += 2
        elif "Service" in company:
            premium_score += 1
        
        if skills_premium["premium_tier"] == "High":
            premium_score += 3
        elif skills_premium["premium_tier"] == "Medium":
            premium_score += 2
        
        if premium_score >= 8:
            return "Premium Market Segment - Top 10%"
        elif premium_score >= 6:
            return "Competitive Market Segment - Top 25%"
        elif premium_score >= 4:
            return "Standard Market Segment - Top 50%"
        else:
            return "Entry Market Segment - Standard positioning"
    
    def _calculate_positioning_score(self, profile: CandidateProfile) -> int:
        """Calculate overall positioning score"""
        score = 0
        
        # Experience scoring
        score += min(int(profile.experience * 10), 40)
        
        # Skills scoring
        if profile.skills:
            score += min(len(profile.skills) * 3, 30)
        
        # Company scoring
        if profile.company:
            company_lower = profile.company.lower()
            if any(t1 in company_lower for t1 in ['google', 'microsoft', 'amazon', 'meta']):
                score += 30
            elif any(t2 in company_lower for t2 in ['flipkart', 'paytm', 'ola']):
                score += 20
            else:
                score += 10
        
        return min(score, 100)
    
    def _identify_advantages(self, profile: CandidateProfile) -> List[str]:
        """Identify competitive advantages"""
        advantages = []
        
        if profile.experience >= 5:
            advantages.append("Senior-level experience with leadership potential")
        
        if profile.skills and len(profile.skills) >= 5:
            advantages.append("Diverse technical skill set")
        
        high_value_skills = ['machine learning', 'system design', 'aws', 'kubernetes']
        if profile.skills and any(skill.lower() in [s.lower() for s in profile.skills] for skill in high_value_skills):
            advantages.append("High-demand technical expertise")
        
        tier1_companies = ['google', 'microsoft', 'amazon', 'meta']
        if profile.company and any(company in profile.company.lower() for company in tier1_companies):
            advantages.append("Premium company background")
        
        if not advantages:
            advantages.append("Standard market positioning")
        
        return advantages
    
    def position_candidate(self, profile: CandidateProfile) -> Dict:
        """Enhanced positioning with detailed analysis"""
        # Transformer-like analysis
        transformer_analysis = self.analyze_with_transformers(profile)
        
        # RAG-enhanced positioning
        rag_query = f"Market positioning for {profile.role} with {profile.experience} years experience at {profile.company}"
        rag_docs = self.rag.retrieve(rag_query, k=3)
        rag_insights = [doc.page_content.strip() for doc in rag_docs]
        
        return {
            "transformer_analysis": transformer_analysis,
            "rag_positioning": rag_insights,
            "final_positioning": transformer_analysis["market_segment"],
            "positioning_score": transformer_analysis["positioning_score"],
            "recommendation": f"Position in {transformer_analysis['market_segment']} with {transformer_analysis['skills_premium']['total_premium']}% skills premium",
            "competitive_advantages": transformer_analysis["competitive_advantages"],
            "market_differentiators": self._get_market_differentiators(profile, transformer_analysis)
        }
    
    def _get_market_differentiators(self, profile: CandidateProfile, analysis: Dict) -> List[str]:
        """Get market differentiators"""
        differentiators = []
        
        if analysis["positioning_score"] > 80:
            differentiators.append("Top-tier candidate with exceptional background")
        elif analysis["positioning_score"] > 60:
            differentiators.append("Strong candidate with competitive positioning")
        else:
            differentiators.append("Solid candidate with growth potential")
        
        if analysis["skills_premium"]["total_premium"] > 30:
            differentiators.append("High-value technical skill set commands premium")
        
        if "Premium" in analysis["market_segment"]:
            differentiators.append("Premium market segment positioning")
        
        return differentiators

class CompensationGeneratorAgent:
    """Agent 3: Compensation generation"""
    
    def __init__(self, api_key: str, rag_retriever: RAGRetriever):
        self.llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=api_key, temperature=0.3)
        self.rag = rag_retriever
    
    def _calculate_base_salary(self, positioning: Dict) -> int:
        """Calculate base salary"""
        base_map = {
            "Junior": 1800000,
            "Mid-level": 3000000, 
            "Senior": 4500000,
            "Staff+": 6500000
        }
        
        experience_tier = positioning.get('experience_analysis', 'Mid-level')
        base = next((v for k, v in base_map.items() if k in experience_tier), 3000000)
        
        # Apply skills premium
        skills_premium = positioning.get('skills_premium', 0)
        return int(base * (1 + skills_premium/100))
    
    def generate_offer(self, market_data: Dict, positioning: Dict) -> Dict:
        """Generate comprehensive offer"""
        base_salary = self._calculate_base_salary(positioning)
        
        # Calculate components
        equity_ratio = 0.3 if "Premium" in positioning.get('market_segment', '') else 0.2
        equity_package = int(base_salary * equity_ratio)
        annual_bonus = int(base_salary * 0.15)
        signing_bonus = int(base_salary * 0.1)
        
        total_comp = base_salary + equity_package + annual_bonus
        
        return {
            "base_salary": base_salary,
            "equity_package": equity_package,
            "annual_bonus": annual_bonus,
            "signing_bonus": signing_bonus,
            "total_compensation": total_comp,
            "package_breakdown": {
                "base_percentage": round((base_salary/total_comp)*100, 1),
                "equity_percentage": round((equity_package/total_comp)*100, 1),
                "bonus_percentage": round((annual_bonus/total_comp)*100, 1)
            },
            "market_position": "Competitive",
            "components_summary": f"Base: ₹{base_salary/100000:.1f}L, Equity: ₹{equity_package/100000:.1f}L, Bonus: ₹{annual_bonus/100000:.1f}L"
        }

class OfferJustificationAgent:
    """Agent 4: Offer justification"""
    
    def __init__(self, api_key: str, rag_retriever: RAGRetriever):
        self.llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=api_key, temperature=0.4)
        self.rag = rag_retriever
    
    def justify_offer(self, offer_data: Dict, candidate_data: Dict, market_data: Dict) -> Dict:
        """Generate offer justification"""
        # Generate scorecard
        scorecard = self._generate_scorecard(offer_data, candidate_data)
        
        # AI justification
        justification = self._create_justification(offer_data, candidate_data, market_data)
        
        return {
            "scorecard": scorecard,
            "detailed_justification": justification,
            "competitive_analysis": self._competitive_analysis(offer_data),
            "recommendation": "APPROVE - Competitive market positioning"
        }
    
    def _generate_scorecard(self, offer_data: Dict, candidate_data: Dict) -> Dict:
        """Generate candidate scorecard"""
        total_comp = offer_data.get('total_compensation', 0)
        
        return {
            "candidate_strength": {
                "experience_score": 85,
                "skills_score": 90,
                "company_background_score": 80,
                "education_score": 75
            },
            "offer_competitiveness": {
                "market_percentile": "70th percentile",
                "total_comp_rating": "Strong" if total_comp > 3000000 else "Competitive",
                "package_balance": "Well-balanced"
            },
            "overall_recommendation": "APPROVE - Strong candidate with competitive offer"
        }
    
    def _create_justification(self, offer_data: Dict, candidate_data: Dict, market_data: Dict) -> str:
        """Create detailed justification"""
        prompt = ChatPromptTemplate.from_template("""
        Create a comprehensive offer justification:
        
        CANDIDATE: {candidate_data}
        OFFER: {offer_data}
        MARKET: {market_data}
        
        Provide 3 paragraphs covering:
        1. Candidate strengths and positioning
        2. Market competitiveness analysis  
        3. Strategic recommendations
        """)
        
        chain = prompt | self.llm | StrOutputParser()
        return chain.invoke({
            "candidate_data": str(candidate_data),
            "offer_data": str(offer_data),
            "market_data": str(market_data)
        })
    
    def _competitive_analysis(self, offer_data: Dict) -> Dict:
        """Competitive analysis"""
        total_comp = offer_data.get('total_compensation', 0)
        
        return {
            "vs_market_average": "+15%" if total_comp > 2500000 else "At market",
            "retention_probability": "High" if total_comp > 3000000 else "Medium",
            "offer_attractiveness": "Very competitive" if total_comp > 3500000 else "Competitive"
        }

# Simplified Multi-Agent Orchestrator
class MultiAgentOrchestrator:
    """Simplified multi-agent orchestration without LangGraph"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.rag_retriever = RAGRetriever(api_key)
        
        # Initialize agents
        self.market_agent = MarketBenchmarkRetrieverAgent(api_key, self.rag_retriever)
        self.positioning_agent = CandidatePositioningAgent(api_key, self.rag_retriever)
        self.compensation_agent = CompensationGeneratorAgent(api_key, self.rag_retriever)
        self.justification_agent = OfferJustificationAgent(api_key, self.rag_retriever)
    
    def generate_complete_offer(self, candidate: CandidateProfile) -> Dict:
        """Execute complete agent pipeline"""
        workflow_messages = ["🚀 Starting multi-agent workflow"]
        
        # Step 1: Market retrieval
        workflow_messages.append("🔍 Agent 1: Retrieving market data...")
        market_data = self.market_agent.retrieve_market_data(
            candidate.role or "Software Engineer",
            candidate.location or "Bangalore", 
            "tech"
        )
        workflow_messages.append("✅ Market data retrieved")
        
        # Step 2: Candidate positioning
        workflow_messages.append("🎯 Agent 2: Positioning candidate...")
        positioning = self.positioning_agent.position_candidate(candidate)
        workflow_messages.append("✅ Candidate positioned")
        
        # Step 3: Compensation generation
        workflow_messages.append("💰 Agent 3: Generating compensation...")
        compensation = self.compensation_agent.generate_offer(market_data, positioning)
        workflow_messages.append("✅ Compensation generated")
        
        # Step 4: Offer justification
        workflow_messages.append("📊 Agent 4: Creating justification...")
        justification = self.justification_agent.justify_offer(
            compensation, candidate.__dict__, market_data
        )
        workflow_messages.append("✅ Pipeline completed successfully!")
        
        return {
            "candidate": candidate.__dict__,
            "market_data": market_data,
            "positioning": positioning,
            "compensation": compensation,
            "justification": justification,
            "workflow_messages": workflow_messages,
            "timestamp": time.time()
        }