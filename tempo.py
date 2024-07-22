progress_text = "Operation en cours. Attendez svp."
        my_bar = st.progress(0, text=progress_text)
        liste_contenu = []
        liste_identifiers_dataset = []
        for i in range(len(Selection_ZA)):
            time.sleep(0.01)
            try:
                s = int(data['ids_niv2'][data['niv2']==Selection_ZA[i]].values)
                datav = api.get_dataverse_contents(s)
                datav_contenu = datav.json()
                if datav_contenu["data"][0]['type']!="dataverse":
                    liste_contenu.append(len(datav_contenu["data"]))
                    st.write(datav_contenu["data"])
                else:
                    st.write(datav_contenu["data"])
                    s = datav_contenu["data"][0]['id']
                    datav_bis = api.get_dataverse_contents(s)
                    datav_contenu_bis = datav_bis.json()
                    st.write(datav_contenu_bis["data"])
                    liste_contenu.append(0)
                try:
                    for i in range(len(datav_contenu["data"])):
                        liste_identifiers_dataset.append(datav_contenu["data"][i]['identifier'])
                except:
                    pass
            except:
                liste_contenu.append(0)
            my_bar.progress(i + 1, text=progress_text)
    
        df = pd.DataFrame(liste_contenu,index=liste_ZAs,columns=['Nombre_dépôts'])
        fig0= go.Figure()
        for i, za in enumerate(df.index.values):
            selec = df.index.values[i:i+1]
            selec_len = df['Nombre_dépôts'].values[i:i+1]
            fig0.add_trace(go.Bar(
                        x=selec,
                        y=selec_len,
                        name=za,
                        marker=dict(color=colors2[i])
                    ))
        fig0.update_layout(
                                title='Nombre de dépôts répertoriées au 06/06/24',
                                width=1000,
                                height=500)
        st.plotly_chart(fig0,use_container_width=True)
        my_bar.empty()


        authority = "10.48579"
        st.write(liste_identifiers_dataset)
        
        for identifier in liste_identifiers_dataset:
            dataset = api.get_dataset(identifier=f"doi:{authority}/{identifier}")
            dataset_ = dataset.json()
            st.write(dataset_["data"]["latestVersion"]["metadataBlocks"]["citation"]["fields"][0]["value"])     