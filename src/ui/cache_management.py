"""
Interface para gerenciamento do cache
"""
import streamlit as st
from src.cache import (
    get_cache_stats, clear_cache, is_cache_enabled,
    enable_cache, disable_cache
)

def show_cache_management():
    """Exibe interface de gerenciamento do cache"""
    st.subheader("🗄️ Gerenciamento de Cache")
    
    # Status do cache
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            "Status do Cache",
            "✅ Ativo" if is_cache_enabled() else "❌ Inativo"
        )
    
    with col2:
        if is_cache_enabled():
            if st.button("❌ Desabilitar Cache", type="primary"):
                disable_cache()
                st.success("Cache desabilitado!")
                st.rerun()
        else:
            if st.button("✅ Habilitar Cache", type="primary"):
                enable_cache()
                st.success("Cache habilitado!")
                st.rerun()
    
    # Estatísticas do cache
    stats = get_cache_stats()
    
    st.subheader("📊 Estatísticas do Cache")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Tamanho Atual", f"{stats['current_size']:,}")
    
    with col2:
        st.metric("Tamanho Máximo", f"{stats['max_size']:,}")
    
    with col3:
        hit_rate = stats['hit_rate'] * 100
        st.metric("Taxa de Acerto", f"{hit_rate:.1f}%")
    
    with col4:
        st.metric("Total de Sets", f"{stats['sets']:,}")
    
    # Detalhes das estatísticas
    with st.expander("📈 Detalhes das Estatísticas"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Hits:**", f"{stats['hits']:,}")
            st.write("**Misses:**", f"{stats['misses']:,}")
            st.write("**Evictions:**", f"{stats['evictions']:,}")
        
        with col2:
            st.write("**Criado em:**", stats['created_at'].strftime('%d/%m/%Y %H:%M'))
            st.write("**Habilitado:**", "Sim" if stats['enabled'] else "Não")
    
    # Ações do cache
    st.subheader("🔧 Ações do Cache")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🗑️ Limpar Cache", type="secondary"):
            clear_cache()
            st.success("Cache limpo com sucesso!")
            st.rerun()
    
    with col2:
        if st.button("🔄 Atualizar Estatísticas", type="primary"):
            st.rerun()
    
    # Informações sobre o cache
    st.subheader("ℹ️ Sobre o Cache")
    
    st.info("""
    **Como funciona o cache:**
    
    - **Consultas frequentes** são armazenadas em memória por 5-10 minutos
    - **Busca unificada** e **estatísticas** são cacheadas para melhor performance
    - **Cache automático** com TTL (Time To Live) configurável
    - **Eviction automático** quando o cache atinge o limite máximo
    
    **Benefícios:**
    - ⚡ Consultas mais rápidas
    - 📉 Menor carga no banco de dados
    - 🎯 Melhor experiência do usuário
    """)
    
    # Configurações do cache
    st.subheader("⚙️ Configurações")
    
    st.warning("""
    **Configurações atuais:**
    - TTL padrão: 5 minutos (300 segundos)
    - TTL estatísticas: 10 minutos (600 segundos)
    - Tamanho máximo: 1.000 itens
    - Eviction: LRU (Least Recently Used)
    """)

def show_cache_performance_metrics():
    """Exibe métricas de performance do cache"""
    stats = get_cache_stats()
    
    # Calcular métricas de performance
    total_requests = stats['hits'] + stats['misses']
    if total_requests > 0:
        hit_rate = (stats['hits'] / total_requests) * 100
        miss_rate = (stats['misses'] / total_requests) * 100
    else:
        hit_rate = 0
        miss_rate = 0
    
    # Exibir métricas
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Taxa de Acerto",
            f"{hit_rate:.1f}%",
            delta=f"{stats['hits']:,} hits"
        )
    
    with col2:
        st.metric(
            "Taxa de Miss",
            f"{miss_rate:.1f}%",
            delta=f"{stats['misses']:,} misses"
        )
    
    with col3:
        efficiency = "Alta" if hit_rate > 70 else "Média" if hit_rate > 40 else "Baixa"
        st.metric(
            "Eficiência",
            efficiency,
            delta=f"{stats['current_size']}/{stats['max_size']} itens"
        )
    
    # Gráfico de performance (se houver dados)
    if total_requests > 0:
        import plotly.express as px
        
        performance_data = {
            'Tipo': ['Hits', 'Misses'],
            'Quantidade': [stats['hits'], stats['misses']],
            'Porcentagem': [hit_rate, miss_rate]
        }
        
        fig = px.pie(
            performance_data, 
            values='Quantidade', 
            names='Tipo',
            title='Distribuição de Hits vs Misses',
            color_discrete_map={'Hits': '#00ff00', 'Misses': '#ff0000'}
        )
        
        st.plotly_chart(fig, use_container_width=True) 